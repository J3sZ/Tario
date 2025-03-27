from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django_tenants.utils import get_tenant_model


user = get_user_model()

class  CustomUserCreationForm(UserCreationForm):
    tenant_name = forms.CharField(max_length=100, label="Nombre de tu negocio: ")
    dominio = forms.CharField(max_length=100, label="Subdominio (ej: tunegocio): ")

    class Meta(UserCreationForm.Meta):
        model = user
        fields = ('username', 'email', 'password1','password2', 'domain_name','tenant_name', )

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': 'Usuario o contraseña incorrectos.',
    }

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
    
        #verifica si el usuario tiene un tenant asociado
        if not hasattr(user, 'tenant') or user.tenant is None:
            raise ValidationError(
                self.error_messages['no_tenant'],
                code='no_tenant',
            )