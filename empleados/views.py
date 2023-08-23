from django.shortcuts import render, reverse
from .forms import EmpleadoModelForm
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from clientes.models import Empleado
from .mixins import *


class EmpleadoListView(OrganisorAndLoginRequiredMixin, ListView):
    template_name = "empleados/lista_empleados.html"

    def get_queryset(self):
#        organisation = self.request.user.userprofile
 #       return Empleado.objects.filter(organisation=organisation)
        return Empleado.objects.all()


class EmpleadoCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    template_name = "empleados/crear_empleado.html"
    form_class = EmpleadoModelForm

    def get_success_url(self):
        return reverse("empleados:lista-empleados")
    def form_valid(self, form):
        empleado = form.save(commit=False)
        empleado.organisation = self.request.user.userprofile
        empleado.save()
        return super(EmpleadoCreateView, self).form_valid(form)

class EmpleadoDetailView(OrganisorAndLoginRequiredMixin, DetailView):
    template_name = "empleados/detalles_empleado.html"
    def get_queryset(self):
#        organisation = self.request.user.userprofile
#        return Empleado.objects.filter(organisation=organisation)
        return Empleado.objects.all()

class EmpleadoUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    template_name = "empleados/editar_empleado.html"
    form_class = EmpleadoModelForm

    def get_success_url(self):
        return reverse("empleados:detalles-empleado", args=[self.kwargs["pk"]])
    def get_queryset(self):
        #organisation = self.request.user.userprofile
        #return Empleado.objects.filter(organisation=organisation)
        return Empleado.objects.all() 


class EmpleadoDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = "empleados/eliminar_empleado.html"

    def get_success_url(self):
        return reverse("empleados:lista-empleados")
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Empleado.objects.filter(organisation=organisation)

