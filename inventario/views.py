from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from inventario.models import *

# Create your views here.

class InventoryCreateView(CreateView):
    template_name = "inventory/object_create.html"
#    form_class

    def get_success_url(self):
        return reverse("inventory:inventory-list")

class InventoryListView(ListView):
    template_name = "inventory/object_list.html"

    def get_context_data(self, **kwargs):
        context = super(InventoryListView, self).get_context_data(**kwargs)
        context.update({
            "tools": Tool.objects.all(),
            "consumables": Consumable.objects.all(),
            })
        return context

class InventoryDetailView(DetailView):
    pass

class InventoryUpdateView(UpdateView):
    pass

class InventoryDeleteView(DeleteView):
    pass
