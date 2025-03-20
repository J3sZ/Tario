from django.contrib import admin
from .models import CustomUser  # Importa el modelo de usuario personalizado

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'tenant')  # Campos a mostrar
    list_filter = ('tenant',)  # Filtros por inquilino
    search_fields = ('username', 'email')  # Campos por los que se puede buscar