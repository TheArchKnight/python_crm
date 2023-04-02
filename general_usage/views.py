from django.forms import formset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.http.response import json
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, FormView, View
from clientes.views import CARPETA_FUMIGACION
from fachadas.views import CARPETA_FACHADAS
from functions import write_file
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
        context['formset'] = PedidoFormSet(queryset=Pedido.objects.none())
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
        formset = PedidoFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.fecha = datetime.today()
            instance.usuario = self.request.user
            if self.kwargs["tipo"] == "obra":
                instance.ubicacion = Obra.objects.get(id=self.kwargs["pk"])
            elif self.kwargs["tipo"] == "visita":
                instance.ubicacion = Visita.objects.get(id=self.kwargs["pk"])
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


       
