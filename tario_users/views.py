# users/views.py
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from tenants.models import Tenant, Domain
from django_tenants.utils import tenant_context
from .forms import CustomUserCreationForm, CustomLoginForm


class RegisterView(View):
    """Handles user registration with tenant creation."""
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm

    def get(self, request, *args, **kwargs):
        """Handles GET requests (shows the registration form)."""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Handles POST requests (processes the registration form)."""
        form = self.form_class(request.POST)
        
        if form.is_valid():
            # 1. Create Tenant
            tenant = Tenant(
                schema_name=form.cleaned_data['domain_name'].lower().replace(" ", "_"),
                name=form.cleaned_data['tenant_name'],
            )
            tenant.save()

            # 2. Create Domain
            domain = Domain(
                domain=f"{form.cleaned_data['domain_name']}.tario.com",
                tenant=tenant,
                is_primary=True,
            )
            domain.save()

            # 3. Create User and assign Tenant
            user = form.save(commit=False)
            user.tenant = tenant
            user.save()

            login(request, user)
            return redirect('home.html')

        return render(request, self.template_name, {'form': form})


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        try:
            user = form.get_user()
            
            # Verificación crítica del tenant
            if not hasattr(user, 'tenant') or user.tenant is None:
                form.add_error(None, "El usuario no tiene tenant asignado")
                return self.form_invalid(form)
            
            # Actualización segura
            user.last_login = timezone.now()
            user.save()
            
            # Configuración de sesión con verificación
            self.request.session['tenant_id'] = user.tenant.id
            
            # Tenant context con manejo de errores
            from django_tenants.utils import tenant_context
            with tenant_context(user.tenant):
                return super().form_valid(form)
                
        except Exception as e:
            # Log del error para diagnóstico
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en login: {str(e)}")
            form.add_error(None, "Error interno durante el acceso")
            return self.form_invalid(form)
        


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'login'  # Página a redirigir después del logout

    def dispatch(self, request, *args, **kwargs):
        # Limpiar información específica del tenant de la sesión
        tenant_id = request.session.pop('tenant_id', None)
        
        # Si hay tenant en sesión, hacer logout en su contexto
        if tenant_id:
            from tenants.models import Tenant  # Reemplaza 'tu_app' con tu app real
            try:
                tenant = Tenant.objects.get(id=tenant_id)
                with tenant_context(tenant):
                    logout(request)
            except Tenant.DoesNotExist:
                logout(request)
        else:
            logout(request)
            
        return redirect(self.next_page)