# inventario/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Item
from django_tenants.utils import get_tenant

@login_required
def add_item(request):
    if request.method == 'POST':
        tenant = get_tenant(request)  # Obtiene el tenant actual del usuario
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        
        # Crea el item asociado al tenant del usuario
        Item.objects.create(
            tenant=tenant,
            name=name,
            quantity=quantity
        )
        return redirect('lista_items')  # Redirige a la lista de items

    return render(request, 'inventory/add_item.html')

@login_required
def lista_items(request):
    tenant = get_tenant(request)  # Obtiene el tenant del usuario
    items = Item.objects.filter(tenant=tenant)  # Filtra items por tenant
    return render(request, 'inventory/item_list.html', {'items': items})