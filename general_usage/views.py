from django.forms import formset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.http.response import json
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView, View
from clientes.views import CARPETA_FUMIGACION
from fachadas.views import CARPETA_FACHADAS
from functions import filter_models, write_file
from general_usage.forms import *
from general_usage.models import *
from fachadas.models import Obra
from clientes.models import Interaccion, Visita
from inventario.models import Subelemento
# Create your views here.
class NotaCreateView(View):
    http_method_names=["post"]

    def post(self, request, **kwargs):
        contenido = request.POST["contenido"]
        fecha = request.POST["fecha"]
        ubicacion = kwargs["tipo"]
        pk = kwargs["pk"]
        link=''
        if ubicacion == "obra":
            fecha = datetime.strptime(fecha, "%Y-%m-%d")
            año_mes = fecha.strftime("%Y-%m")
            dia = fecha.strftime("%d") 
            ubicacion = Obra.objects.get(id=pk)
            link = reverse("fachadas:detalles-obra", args=[pk, año_mes, dia])
        elif ubicacion == "interaccion":
            ubicacion = Interaccion.objects.get(id=pk)
            link = reverse("clientes:detalles-cliente", args=[pk])

        Nota.objects.create(ubicacion=ubicacion, contenido=contenido, usuario=request.user)
        return redirect(link)

class ArchivoCreateView(View):

    http_method_names = ["post"]

    def post(self, request, **kwargs):
        files = request.FILES.getlist("files")
        fecha = request.POST["fecha"]
        ubicacion = kwargs["tipo"]
        pk = kwargs["pk"]
        path = f""
        link = ""
        if ubicacion == "obra":
            ubicacion = Obra.objects.get(id=pk)
            fecha = datetime.strptime(fecha, "%Y-%m-%d")
            año_mes = fecha.strftime("%Y-%m")
            dia = fecha.strftime("%d")
            link = reverse("fachadas:detalles-obra", args=[pk, año_mes, dia])
            path = f"{CARPETA_FACHADAS}{ubicacion.nombre_obra}/{año_mes}/{dia}"
        elif ubicacion == "interaccion":
            ubicacion = Visita.objects.get(id=pk)
            cliente = ubicacion.cliente
            link = reverse("clientes:detalles-cliente", args=[cliente.id])
            path = f"{CARPETA_FUMIGACION}/{cliente.nombre_orgnanizacion}/{ubicacion.fecha}"
        write_file(files, path, ubicacion, request.user)
        return(redirect(link))


class PedidoFormsetView(CreateView):
    model =  Pedido
    form_class = PedidoModelForm
    template_name = "general_usage/crear_pedido.html"


    def get_context_data(self, **kwargs):
        context = super(PedidoFormsetView, self).get_context_data(**kwargs)
        previous = self.get_success_url()
        context['formset'] = PedidoFormSetCreate(queryset=Pedido.objects.none())
        context['previous'] = previous
        return context
    def get_success_url(self):
        link = ''
        if self.kwargs["tipo"] == "obra":
            fecha = datetime.strptime(self.kwargs["fecha"], "%Y-%m-%d").date()
            año_mes = fecha.strftime("%Y-%m")
            dia = fecha.strftime("%d")
            link = reverse("fachadas:detalles-obra", kwargs={"obra_pk":
                                                             self.kwargs["pk"],
                                                             "año_mes":año_mes,
                                                             "dia":dia
                                                             })
        elif self.kwargs["tipo"] == "visita":
            link = reverse("clientes:detalles-cliente", args=[self.kwargs["pk"]])
        return link

    def post(self, request, *args, **kwargs):
        formset = PedidoFormSetCreate(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        instances = formset.save(commit=False)
        grupo_pedido = Grupo_Pedido()
        grupo_pedido.usuario = self.request.user
        if self.kwargs["tipo"] == "obra":
            grupo_pedido.ubicacion = Obra.objects.get(id=self.kwargs["pk"])
        elif self.kwargs["tipo"] == "visita":
            grupo_pedido.ubicacion = Visita.objects.get(id=self.kwargs["pk"])
        grupo_pedido.save()
        for instance in instances:
            instance.grupo_pedido = grupo_pedido
            instance.save()
        return HttpResponseRedirect(self.get_success_url())


# AJAX
def cargar_subelementos(request):
    try:
        elemento_id= json.load(request)["elemento_id"]
        subelementos = Subelemento.objects.filter(elemento_id=elemento_id)
        return JsonResponse(list(subelementos.values('id', 'codigo_unico', 'marca')), safe=False)

    except ValueError:
        return JsonResponse(list(), safe=False)

class PedidoDetailView(DetailView):
    model=Grupo_Pedido
    form_class = PedidoModelForm
    pk_url_kwarg="pedido_pk"
    template_name="general_usage/detalles-pedido.html"
    context_object_name = "grupo_pedido"

    def get_success_url(self):
        return reverse("inventario:lista-elementos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grupo_pedido = Grupo_Pedido.objects.get(id=self.kwargs[self.pk_url_kwarg])
        elementos_pedido = Pedido.objects.filter(grupo_pedido=grupo_pedido)
        formset = PedidoFormSetUpdate(queryset=elementos_pedido)
        elementos_pedido = zip(elementos_pedido, formset)
        context.update({"grupo_pedido":grupo_pedido,
                        "elementos_pedido":elementos_pedido,
                        "previous":self.get_success_url()})
        return context

    def post(self, request, *args, **kwargs):
        grupo_pedido = self.get_object()
        elementos_pedido =  Pedido.objects.filter(grupo_pedido=grupo_pedido)
        forms = request.POST
        print(forms)
        for i in range(len(elementos_pedido)):
            elementos_pedido[i].cantidad_enviada = int(forms["form-"+str(i)+"-cantidad_enviada"])
            elementos_pedido[i].estado = "DESPACHADO" 
            elementos_pedido[i].save()
        grupo_pedido.estado = "FINALIZADO"
        grupo_pedido.save()
        return HttpResponseRedirect(self.get_success_url())

class ObjetoListView(ListView):
    template_name = "general_usage/lista_objetos.html"
    model = Objeto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ubicacion = self.kwargs["tipo"]
        if ubicacion == "obra":
            ubicacion = ContentType.objects.get_for_model(Obra)
        elif ubicacion == "visita":
            ubicacion = ContentType.objects.get_for_model(Visita)
        objetos = Objeto.objects.filter(content_type__pk=ubicacion.id).order_by("-fecha")
        list_models = [Archivo,Nota,Grupo_Pedido]
        objetos = filter_models(list_models, objetos)
        
        context.update({
            "objetos": objetos,
            })
        return context



