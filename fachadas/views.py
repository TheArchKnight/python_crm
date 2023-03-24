from datetime import datetime
import os
from shutil import rmtree
from django.shortcuts import redirect, render, reverse
from django.views.generic import CreateView, DeleteView, FormView, ListView
from clientes.models import Empleado
from fachadas.models import *
from fachadas.forms import *
from fachadas.functions import *
# Create your views here.

CARPETA_FACHADAS = "/home/anorak/Test/Fachadas/"


class ObraListView(ListView):
    template_name = "fachadas/lista_fachadas.html"

    def get_queryset(self):
        return Obra.objects.all()


    def get_context_data(self, **kwargs):
        context = super(ObraListView, self).get_context_data(**kwargs)
        obras = Obra.objects.all()
        urls = [reverse("fachadas:eliminar-obra", args=[i.id]) for i in obras]
        obras = zip(obras, urls)
        fecha = date.today()
        context.update({
            "año_mes": fecha.strftime("%Y-%m"),
            "dia":fecha.strftime("%d"),
            "obras": obras
            })
        return context

class ObraCreateView(CreateView):
    template_name ="fachadas/iniciar_obra.html"
    form_class = ObraModelForm

    def get_success_url(self):
        return reverse("fachadas:lista-obra")

    def get_context_data(self, **kwargs):
        context = super(ObraCreateView, self).get_context_data(**kwargs)
        context.update({
            "previous":reverse("fachadas:lista-obra")

            })
        return context 

    def form_valid(self, form):
        form.instance.empelado = Empleado.objects.get(user=self.request.user)
        os.mkdir(CARPETA_FACHADAS + form.instance.nombre_obra)
        return super(ObraCreateView, self).form_valid(form)

class ObraDetailView(FormView):
    template_name = "fachadas/detalles_obra.html"
    form_class = MesForm

    def get_success_url(self):
        return reverse("fachadas:detalles-obra", args=[self.kwargs["obra_pk"]])

    def get_context_data(self, **kwargs):
        context = super(ObraDetailView, self).get_context_data(**kwargs)
        trabajadores = Trabajador.objects.filter(obra_id = self.kwargs["obra_pk"])
        obra = Obra.objects.get(id=self.kwargs["obra_pk"])
        dict_fecha = unir_fecha(self.kwargs)
        #Get all the costs, no matter the date 
        costos = Costo.objects.filter(obra = obra).order_by("-fecha")
        #filter the costs searching for the ones of an exact day of a month
        costos_display = costos.filter(fecha=dict_fecha["fecha"])
        #queryset of costs related to a certain month and year
        costos_mes = costos.filter(fecha__year=dict_fecha["fecha"].year, fecha__month=dict_fecha["fecha"].month)
        dias_mes = [i["fecha"].strftime("%d") for i in costos_mes.values("fecha").annotate(n = models.Count("pk"))]  
        meses_unicos = [i["fecha"].strftime("%Y-%m") for i in costos.values("fecha").annotate(n = models.Count("pk"))]
        meses_unicos = valores_unicos(meses_unicos)
        try:
            meses_unicos.remove(dict_fecha["año_mes"])
        except:
            pass
        meses_unicos.insert(0, dict_fecha["año_mes"])
        #expenses to be disaplayed on the web page
        costos_display = asignar_acciones(costos_display, obra, dict_fecha["fecha"])

        context.update({
            "previous":reverse("fachadas:lista-obra"),
            "obra":obra,
            "trabajadores": trabajadores,
            "costos":costos_display,
            "dias":dias_mes,
            "dict_fecha":dict_fecha,
            "meses_unicos":meses_unicos
            })
        return context

class ObraDeleteView(DeleteView):
    model = Obra
    http_method_names = ['delete']

    def dispatch(self, request, *args, **kwargs):
        instance = Obra.objects.get(id=self.kwargs["pk"])
        rmtree(CARPETA_FACHADAS + instance.nombre_obra)
        handler = getattr(self, 'delete')
        return handler(request, *args, **kwargs)

    def get_success_url(self):
        success_url = str(reverse('fachadas:lista-obra'))
        return success_url

def pagar_nomina(request, pk, año_mes, dia):
    obra = Obra.objects.get(id=pk)
    trabajadores = Trabajador.objects.filter(obra=obra)
    if request.method == "POST":
        inicio_nomina = request.POST["inicio_nomina"] 
        final_nomina = request.POST["final_nomina"]
        for trabajador in trabajadores:
            acciones = Accion.objects.filter(trabajador=trabajador, fecha__gte=inicio_nomina, fecha__lte=final_nomina)
            valor_nomina = sum([i.precio_unidad * i.cantidad for i in acciones])
            trabajador.acumulado -= valor_nomina
            trabajador.ultimo_pago = valor_nomina
            trabajador.save()

    return redirect(reverse("fachadas:detalles-obra", args=[pk, año_mes, dia]))

class CostoCreateView(FormView):
    template_name = "fachadas/crear_costo.html"
    form_class=CostoForm
    
    def get_success_url(self):
        dict = unir_fecha(self.kwargs)
        return reverse("fachadas:detalles-obra", args=[self.kwargs["pk"], dict["año_mes"], dict["dia"]])


    def get_form_kwargs(self):
        #pass kwarg with last visit
        kwargs = super().get_form_kwargs()
        kwargs["obra"] = Obra.objects.get(id=self.kwargs["pk"])
        return kwargs

    def get_context_data(self, **kwargs):
        dict = unir_fecha(self.kwargs)
        context = super(CostoCreateView, self).get_context_data(**kwargs)
        context.update({
            "previous":reverse("fachadas:detalles-obra", args=[self.kwargs["pk"], dict["año_mes"], dict["dia"]])
            })
        return context

    def form_valid(self, form):
        descripcion = form.cleaned_data["descripcion"]
        cantidad = form.cleaned_data["cantidad"]
        fecha = form.cleaned_data["fecha"]
        precio_unidad = form.cleaned_data["precio_unidad"]
        cobro_unidad = form.cleaned_data["cobro_unidad"]
        obra = Obra.objects.get(id=self.kwargs["pk"])
        trabajador = form.cleaned_data["trabajador"]
        
        obra.costo_total += precio_unidad * cantidad
        obra.save()

        if form.cleaned_data["tipo"] == "COSTO":
            Costo.objects.create(descripcion=descripcion, cantidad=cantidad, fecha=fecha, obra=obra, precio_unidad=precio_unidad, cobro_unidad=cobro_unidad)
        elif form.cleaned_data["tipo"] == "ACCION":
            Accion.objects.create(descripcion=descripcion, cantidad=cantidad, fecha=fecha, obra=obra, precio_unidad=precio_unidad, cobro_unidad=cobro_unidad, trabajador=trabajador)
            trabajador.acumulado += precio_unidad * cantidad
            trabajador.save()

        return super().form_valid(form)

class TrabajadorCreateView(CreateView):
    template_name="fachadas/crear_trabajador.html"
    form_class = TrabajadorModelForm


    def get_success_url(self):
        dict = unir_fecha(self.kwargs)
        return reverse("fachadas:detalles-obra", args=[self.kwargs["pk"], dict["año_mes"], dict["dia"]])


    def get_context_data(self, **kwargs):
        context = super(TrabajadorCreateView, self).get_context_data(**kwargs)
        dict = unir_fecha(self.kwargs)
        context.update({
            "previous":reverse("fachadas:detalles-obra", args=[self.kwargs["pk"], dict["año_mes"], dict["dia"]]) 
            })
        return context

    def form_valid(self, form):
        obra = Obra.objects.get(id=self.kwargs["pk"])
        form.instance.obra = obra
        return super().form_valid(form)

