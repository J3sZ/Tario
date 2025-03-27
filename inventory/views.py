# inventario/views.py
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item
from django_tenants.utils import get_tenant

class AddItemView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'inventory/add_item.html'
    fields = ['name', 'quantity']
    success_url = reverse_lazy('lista_items')

    def form_valid(self, form):
        # Asigna automáticamente el tenant del usuario al item
        form.instance.tenant = get_tenant(self.request)
        return super().form_valid(form)
    
class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'inventory/item_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        # Filtra los items por el tenant del usuario
        return Item.objects.filter(tenant=get_tenant(self.request))