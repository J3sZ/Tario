from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


user = get_user_model()

class  CustomUserCreationForm(UserCreationForm):
    tenant_name = forms.CharField(max_length=100, label="Nombre de tu negocio: ")
    dominio = forms.CharField(max_length=100, label="Subdominio (ej: tunegocio): ")

    class Meta(UserCreationForm.Meta):
        model = user
        fields = ('username', 'email', 'password1','password2', 'domain_name','tenant_name', )