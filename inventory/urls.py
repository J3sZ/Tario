# inventario/urls.py
from django.urls import path
from .views import add_item, lista_items

urlpatterns = [
    path('add/', add_item, name='add_item'),
    path('list/', lista_items, name='lista_items'),
]