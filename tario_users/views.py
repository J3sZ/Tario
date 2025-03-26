# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from tenants.models import Tenant, Domain
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # 1. Crea el Tenant
            tenant = Tenant(
                schema_name=form.cleaned_data['domain_name'].lower().replace(" ", "_"),
                name=form.cleaned_data['tenant_name'],
            )
            tenant.save()  # Se guarda en la tabla `tenants_tenant`

            # 2. Crea el Domain
            domain = Domain(
                domain=f"{form.cleaned_data['domain_name']}.tario.com",
                tenant=tenant,
                is_primary=True,
            )
            domain.save()  # Se guarda en la tabla `tenants_domain`

            # 3. Crea el usuario y asígnale el tenant
            user = form.save(commit=False)
            user.tenant = tenant  # Asigna el tenant al usuario
            user.save()  # Se guarda en la tabla `users_customuser`

            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})