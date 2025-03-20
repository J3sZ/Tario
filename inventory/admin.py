from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'tenant')  # Muestra el tenant en la lista
    list_filter = ('tenant',)  # Filtra por tenant
    search_fields = ('name',)  # Busca por nombre