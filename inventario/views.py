
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView
from general_usage.models import Grupo_Pedido

from inventario.models import *
from inventario.forms import *

class ElementoListView(ListView):
    template_name="inventario/lista_elementos.html"
    queryset = Elemento.objects.all().order_by("-codigo_general")
    object_list = Elemento.objects.all() 
    context_object_name = "elementos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pedidos = Grupo_Pedido.objects.filter(estado="EN PROCESO")
        context.update({"pedidos":pedidos})
        return context

    def post(self, request, **kwargs):
        searched = request.POST["searched"]
        filtro = request.POST["filtro"]
        elementos = []
        if filtro == "descripcion":
            elementos = Elemento.objects.filter(descripcion__icontains=searched)
        elif filtro == "codigo":
            elementos = Elemento.objects.filter(codigo_general__icontains=searched)
        context = {"elementos":elementos}
        return super(ElementoListView, self,).render_to_response(context)
    
class ElementoDetailView(FormView):
    template_name="inventario/detalles_elemento.html"
    form_class = SubelementoModelForm

    def get_success_url(self):
        return reverse("inventario:detalles-elemento", args=[self.kwargs["elemento_pk"]])

    def get_context_data(self, **kwargs):
        context = super(ElementoDetailView, self).get_context_data(**kwargs)
        elemento = Elemento.objects.get(id=self.kwargs["elemento_pk"])
        subelementos = Subelemento.objects.filter(elemento=elemento)
        urls = [reverse("inventario:eliminar-subelemento", args=[self.kwargs["elemento_pk"], i.id]) for i in subelementos]
        subelementos = zip(subelementos, urls)
        context.update({
            "elemento":elemento,
            "subelementos": subelementos,
            "previous": reverse("inventario:lista-elementos")
            })
        return context

    def form_valid(self, form):
        elemento = Elemento.objects.get(id=self.kwargs["elemento_pk"])
        form.instance.elemento =elemento
        form.save()
        return super().form_valid(form)


class ElementoCreateView(CreateView):
    template_name = "inventario/crear_elemento.html"
    model = Elemento
    form_class = ElementoModelForm

    def get_success_url(self):
        return reverse("inventario:lista-elementos")

    def get_context_data(self, **kwargs):
        context = super(ElementoCreateView, self).get_context_data(**kwargs)
        context.update(
                {"previous":reverse("inventario:lista-elementos")})
        return context

class ElementoUpdateView(UpdateView):
    template_name="inventario/editar_elemento.html"
    model = Elemento
    form_class = ElementoModelForm
    pk_url_kwarg = "elem_pk"

    def get_success_url(self):
        return reverse("inventario:detalles-elemento", args=[self.kwargs["elem_pk"]])
    def get_context_data(self, **kwargs):
        context = super(ElementoUpdateView, self).get_context_data(**kwargs)
        context.update({
            "previous": reverse("inventario:detalles-elemento", args=[self.kwargs["elem_pk"]])    
            })
        return context

class ElementoDeleteView(DeleteView):
    model = Elemento
    http_method_names = ['delete']
    pk_url_kwarg = "elem_pk"

    def dispatch(self, request, *args, **kwargs):
        handler = getattr(self, 'delete')
        return handler(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('inventario:lista-elementos')

class SubelementoUpdateView(UpdateView):
    template_name = "inventario/editar_subelemento.html"
    model = Subelemento
    form_class = SubelementoModelForm
    pk_url_kwarg = "sub_pk"

    def get_success_url(self):
        return reverse("inventario:detalles-elemento", args=[self.kwargs["elem_pk"]])
    def get_context_data(self, **kwargs):
        context = super(SubelementoUpdateView, self).get_context_data(**kwargs)
        context.update({
            "previous": reverse("inventario:detalles-elemento", args=[self.kwargs["elem_pk"]])    
            })
        return context

class SubelementoDeleteView(DeleteView):
    model = Subelemento
    http_method_names = ['delete']
    pk_url_kwarg = "sub_pk"

    def dispatch(self, request, *args, **kwargs):
        handler = getattr(self, 'delete')
        return handler(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('inventario:detalles-elemento', args=[self.kwargs["elem_pk"]])



