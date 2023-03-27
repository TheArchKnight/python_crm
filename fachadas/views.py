from datetime import datetime
import os
from shutil import rmtree
from django.shortcuts import redirect, render, reverse
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView
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

class ObraDetailView(DetailView):
    template_name = "fachadas/detalles_obra.html"
    pk_url_kwarg = "obra_pk"
    queryset = Obra.objects.all()

    def get_success_url(self):
        return reverse("fachadas:detalles-obra", args=[self.kwargs["obra_pk"]])

    def get(self, request, *args, **kwargs):
        if kwargs["dia"] == "32":
            obra = self.get_object()
            dict_fecha = unir_fecha(kwargs) 
            costos_dict = costos_mes(dict_fecha, obra)
            dia_maximo = costos_dict["dias_mes"][0]
            return redirect("fachadas:detalles-obra", self.kwargs["obra_pk"], self.kwargs["año_mes"], dia_maximo)
        return super(ObraDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ObraDetailView, self).get_context_data(**kwargs)
        obra = self.get_object()
        trabajadores = Trabajador.objects.filter(obra = obra)
        pagos = Pago.objects.filter(obra=obra, fecha=obra.fecha_ultimo_pago)
        try:
            pagos = [pagos.get(trabajador=i) for i in trabajadores] 
        except:
            pass
        trabajadores_pagos = zip(trabajadores, pagos)

        dict_fecha = unir_fecha(self.kwargs)
        costos_dict = costos_mes(dict_fecha, obra)
        costos_display = costos_dict["costos"].filter(fecha=dict_fecha["fecha"]) 
        meses_unicos = [i["fecha"].strftime("%Y-%m") for i in costos_dict["costos"].values("fecha").annotate(n = models.Count("pk"))]
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
            "dias":costos_dict["dias_mes"],
            "dict_fecha":dict_fecha,
            "meses_unicos":meses_unicos,
            "trabajadores_pagos":trabajadores_pagos
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
            obra.fecha_ultimo_pago = date.today() 
            Pago.objects.create(fecha=date.today(), monto=valor_nomina, periodo_inicio=inicio_nomina, periodo_final=final_nomina, trabajador=trabajador, obra=obra)
            trabajador.save()
            obra.save()

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


def filtrar_pagos(request, obra_pk):
    obra = Obra.objects.get(id=obra_pk)
    pagos = []
    if request.method == "POST":
        inicio_pago = request.POST["inicio_pago"] 
        final_pago = request.POST["final_pago"]
        periodo = inicio_pago + "/" + final_pago
        pagos = Pago.objects.filter(obra=obra, periodo=periodo)
        return redirect(reverse("fachadas:filtrar-pagos", args=[obra_pk]))
    return render(request, "fachadas/filtrar_pagos.html", {
           "pagos": pagos,
           "obra": obra,
           })


