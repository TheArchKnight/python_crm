from django.shortcuts import render, reverse
from .forms import EmpleadoModelForm
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from clientes.models import Cliente, Empleado, Interaccion
from .mixins import *

class EmpleadoListView(OrganisorAndLoginRequiredMixin, ListView):
    template_name = "empleados/lista_empleados.html"
    context_object_name = "empleados"
    def get_queryset(self):
#        organisation = self.request.user.userprofile
 #       return Empleado.objects.filter(organisation=organisation)
        return Empleado.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context =super().get_context_data(object_list=object_list, **kwargs)
        empleados = self.get_queryset()
        ultimas_interacciones = []
        for empleado in empleados:
          interaccion = Interaccion.objects.filter(empleado__id=empleado.id).order_by("-fecha_creacion")
          ultimas_interacciones.append(interaccion[0])
        
        context.update({
          "empleados_interacciones": zip(empleados, ultimas_interacciones)
          })
        return context

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

    def post(self, request, **kwargs):
        searched = request.POST["searched"]
        filtro = request.POST["filtro"]
        interacciones = Interaccion.objects.none()
        if filtro == "cliente":
          clientes = Cliente.objects.filter(nombre_orgnanizacion__icontains=searched)
          for cliente in clientes:
            print(cliente)
            interacciones = interacciones | Interaccion.objects.filter(cliente__id=cliente.id, empleado__id=self.kwargs["pk"])
        else:
            interacciones = Interaccion.objects.filter(empleado__id=self.kwargs["pk"])
        interacciones.order_by("-fecha_creacion")
        context = {
          "empleado_detalles": reverse("empleados:detalles-empleado", args=[self.kwargs["pk"]]),
          "previous": reverse("empleados:lista-empleados"),
          "empleado": Empleado.objects.get(id=self.kwargs["pk"]),
          "interacciones": interacciones 
          }
        return super(EmpleadoDetailView, self,).render_to_response(context)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.object
        print(self.request.GET)
        interacciones = Interaccion.objects.filter(empleado__id = queryset.id).order_by("-fecha_creacion")
        context.update({
          "empleado_detalles": reverse("empleados:detalles-empleado", args=[self.kwargs["pk"]]),
          "previous": reverse("empleados:lista-empleados"),
          "interacciones": interacciones,
          })
        return context 

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
