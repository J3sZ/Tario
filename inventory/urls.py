# inventario/urls.py
from django.urls import path
from .views import AddItemView, ItemListView


app_name = 'inventory'

urlpatterns = [
    path('add/', AddItemView.as_view(), name='add'),
    path('list/', ItemListView.as_view(), name='list'),
]