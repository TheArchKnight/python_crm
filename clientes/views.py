from datetime import date, timedelta
from shutil import rmtree
from dateutil import relativedelta as rd

from django.contrib.auth.views import LoginView, reverse_lazy
#from django.http import HttpResponseForbidden, request
from django.shortcuts import HttpResponse, redirect, render


from django.urls import reverse
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView
from clientes.functions import *
from clientes.mixins import EmpleadoRequiredMixin
from functions import *

#from clientes.forms import ClienteForm
from .models import Cliente, Empleado, Llamada
from .models import Visita
from .forms import * 

import os
import json

CARPETA_FUMIGACION = "/home/anorak/Test/Fumigacion/"


class SingupView(CreateView):
    template_name="registration/register.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("landing-page")
    def form_valid(self,form):
        if form.instance.fumigacion or form.instance.inventario or form.instance.fachadas:
            form.instance.is_organisor = False
        form.save()
        return super().form_valid(form)

class LandingPageView(LoginView):
    form_class = LoginForm  
    template_name = "landing.html"

    def get(self, request, *args, **kwargs):
        #Redirect user to the clients app if it's authenticated.
        if request.user.is_authenticated:
            if request.user.fachadas:
                return redirect("fachadas:lista-obra")
            elif request.user.fumigacion:
                return redirect("clientes:lista-cliente")
        return super(LandingPageView, self).get(request, *args, **kwargs)

class ClienteListView( EmpleadoRequiredMixin ,ListView):
    template_name = "clientes/lista_clientes.html"
    context_object_name = "clientes"
    queryset = Cliente.objects.all()   
    object_list = Cliente.objects.all()

    def post(self, request, **kwargs):
        searched = request.POST["searched"]
        filtro = request.POST["filtro"]
        clientes = []
        if filtro == "nombre":
            clientes = self.object_list.filter(nombre_orgnanizacion__icontains=searched)
        elif filtro == "administrador":
            clientes = self.object_list.filter(administrador__icontains=searched)
        context = {"clientes":clientes}
        return super(ClienteListView, self,).render_to_response(context)


#This view provides details of the client model, as well as 
#allows the user to create new visits. For this, a creatview class
#is used, and the context is updated with the necessary data for the forms
#and the details of data to work.
class ClienteDetailView(EmpleadoRequiredMixin, FormView):
    template_name = "clientes/detalles_clientes.html"
    form_class= InteraccionForm
   
    def get_success_url(self):
        #Args receives a list with arguments
        return reverse("clientes:detalles-cliente", args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        visitas_cliente = Visita.objects.filter(cliente_id=self.kwargs["pk"]).order_by("-fecha")
        llamadas = Llamada.objects.filter(cliente_id=self.kwargs["pk"]).order_by("-fecha")
        interacciones_cliente= sorted(list(visitas_cliente) + list(llamadas), key=lambda x: x.fecha, reverse=True)
        tipos = [definir_tipos(i) for i in interacciones_cliente]
        visibilidades = ["disabled" if i.fecha > date.today() else "" for i in interacciones_cliente]
        interacciones_cliente = zip(interacciones_cliente, tipos, visibilidades)
        
        visitas_vigentes = Visita.objects.filter(fecha__gte = datetime.today()).values("fecha", "cliente__nombre_orgnanizacion")
#        fechas_usadas = [i.fecha.strftime("%Y-%m-%d") for i in visitas_vigentes]
        for i in visitas_vigentes:
            i["fecha"] = i["fecha"].strftime("%Y-%m-%d")

        #Update the context with our necessary queries
        context.update({
            "visitas_cliente": visitas_cliente,
            "llamadas": llamadas,
            "interacciones_cliente": interacciones_cliente,
            "cliente":Cliente.objects.get(id=self.kwargs["pk"]),
            "previous":reverse("clientes:lista-cliente"), #Link to back button on navbar
            #"fechas_usadas":fechas_usadas,
            "visitas_vigentes":json.dumps(list(visitas_vigentes))
            }) 
        return context

    def get_form_kwargs(self):
        #pass kwarg with last visit
        kwargs = super().get_form_kwargs()
        kwargs["ultima_visita"] = Visita.objects.filter(cliente_id=self.kwargs["pk"]).order_by("-fecha").first()
        return kwargs

    #Manually setting values for the form
    def form_valid(self, form):
        cliente = Cliente.objects.get(id=self.kwargs["pk"])
        visitas = Visita.objects.filter(cliente_id=self.kwargs["pk"]).order_by("-fecha")
        fecha = form.cleaned_data["fecha"]
        observaciones = form.cleaned_data["observaciones"]
    #our form is a generic one which can be used for creating multiple subclasses of the interaction parent class
        if form.cleaned_data["tipo"] == "VISITA":
            carpeta = fecha.strftime('%Y-%m-%d')
            Visita.objects.create(fecha=fecha, observaciones=observaciones, cliente=cliente)
            if visitas.count() == 0:
                cliente.estado = "ACTIVO"
            cliente.rechazos = 0
            
            ruta = os.path.join(CARPETA_FUMIGACION, cliente.nombre_orgnanizacion, carpeta)
            create_folder(ruta)
            if cliente.estado == "INACTIVO":
                cliente.estado = "ACTIVO"
            cliente.save()

        elif form.cleaned_data["tipo"] == "LLAMADA":
            Llamada.objects.create(fecha=fecha, observaciones=observaciones, cliente=cliente)
   

        return super().form_valid(form)
        
class ClienteCreateView(EmpleadoRequiredMixin, CreateView):
    template_name = "clientes/crear_cliente.html"
    form_class=ClienteModelForm

    def get_success_url(self):
        return reverse("clientes:lista-cliente")
    
    def get_form_kwargs(self):
        #pass user instance as an argument for the form
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ClienteCreateView, self).get_context_data(**kwargs)
        context.update({
            "previous":reverse("clientes:lista-cliente")
            })
        return context

    def form_valid(self, form):
        #Allow organisor users to assing clients to agents.
        if self.request.user.is_organisor:
            empleado_username = form.cleaned_data["empleado_field"]
            form.instance.empleado = Empleado.objects.get(user__username = empleado_username)
        else:
            form.instance.empleado = Empleado.objects.get(user = self.request.user)
        ruta = os.path.join(CARPETA_FUMIGACION, form.instance.nombre_orgnanizacion)
        create_folder(ruta)
        
    
        return super(ClienteCreateView, self).form_valid(form)

class ClienteUpdateView(EmpleadoRequiredMixin, UpdateView):
    template_name = "clientes/actualizar_cliente.html"
    queryset = Cliente.objects.all()
    form_class = ClienteModelForm

    def get_success_url(self):
        #The details-client function receives 2 arguments: request and the pk.
        return reverse("clientes:detalles-cliente", args=[self.kwargs['pk']])

    def get_form_kwargs(self):
        #ppas user instance as a kwarg, for form edition.
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ClienteUpdateView, self).get_context_data(**kwargs)
        #Update the context with our necessary queries
        context.update({
            "previous":reverse("clientes:detalles-cliente", args=[self.kwargs["pk"]]) #Link to back button on navbar
            })
        return context


    def form_valid(self, form):
        #TODO send email
        if self.request.user.is_organisor:
            empleado_username = form.cleaned_data["empleado_field"]
            form.instance.empleado = Empleado.objects.get(user__username = empleado_username)
        src = os.path.join(CARPETA_FUMIGACION, self.get_object().nombre_orgnanizacion)
        dst = os.path.join(CARPETA_FUMIGACION, form.instance.nombre_orgnanizacion)
        os.rename(src, dst)

        return super(ClienteUpdateView, self).form_valid(form) 


class ClienteDeleteView(EmpleadoRequiredMixin, DeleteView):

    model = Cliente
    http_method_names = ['delete']

    def dispatch(self, request, *args, **kwargs):
        instance = Cliente.objects.get(id=self.kwargs["pk"])
        carpeta = os.path.join(CARPETA_FUMIGACION, instance.nombre_orgnanizacion)
        try:
            rmtree(carpeta)
        except:
            pass

        handler = getattr(self, 'delete')
        return handler(request, *args, **kwargs)

    def get_success_url(self):
        success_url = str(reverse_lazy('clientes:lista-cliente'))
        return success_url


class VisitaUpdateView(EmpleadoRequiredMixin, UpdateView):
    template_name = "visitas/editar_visita.html"
    queryset = Visita.objects.all()
    form_class = InteraccionForm

    def get_context_data(self, **kwargs):
        context = super(VisitaUpdateView, self).get_context_data(**kwargs)
        #Update the context with our necessary queries
        context.update({
            "cliente":Cliente.objects.filter(visita = self.kwargs["pk"]).first()
            })        
        return context

    def get_success_url(self):
        return reverse("clientes:detalles-cliente", args=[Cliente.objects.get(visita = self.kwargs["pk"]).id])


class VisitaDeleteView(EmpleadoRequiredMixin, DeleteView):
#    template_name = "visitas/eliminar_visita.html"
#    queryset = Visita.objects.all()
   
    model = Visita
    http_method_names = ['delete']

    def dispatch(self, request, *args, **kwargs):
        handler = getattr(self, 'delete')
        return handler(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VisitaDeleteView, self).get_context_data(**kwargs)
        #Update the context with our necessary queries
        context.update({
            "cliente":Cliente.objects.filter(visita = self.kwargs["pk"]).first()
            })        
        return context

    def get_success_url(self):
        return reverse("clientes:detalles-cliente", args=[Cliente.objects.filter(visita = self.kwargs["pk"]).first().id])

#def search_clientes(request):
#    if request.method == "POST":
#        searched = request.POST["searched"]
#        clientes = Cliente.objects.filter(nombre_orgnanizacion__icontains=searched)
#        return render(request, "search_clientes.html", {"searched": searched, "clientes": clientes})
#    else:
#        return render(request, "search_clientes.html", {})

def finalizar_visita(request, pk):
    visita = Visita.objects.get(id=pk)
    visita.estado = "FINALIZADA"
    visita.save()
    cliente = Cliente.objects.get(id=visita.cliente.pk)
    cliente.fecha_vencimiento = visita.fecha + rd.relativedelta(months=cliente.frecuencia_meses)
    fecha_garantia = visita.fecha + rd.relativedelta(days=15)
    if fecha_garantia.weekday() > 4:
        fecha_garantia += timedelta(days=7-fecha_garantia.weekday())
    if cliente.fecha_vencimiento.weekday() > 4:
        cliente.fecha_vencimiento += timedelta(days=7-cliente.fecha_vencimiento.weekday())
    
    Llamada.objects.create(fecha=cliente.fecha_vencimiento, observaciones = "VENCIMIENTO TERMINOS", cliente = cliente)

    Llamada.objects.create(fecha=fecha_garantia, observaciones = "SEGUIMIENTO GARANTIA", cliente = cliente)
    cliente.save()
    return redirect(reverse("clientes:detalles-cliente", args=[cliente.id]))

def finalizar_llamada(request, pk):
    llamada = Llamada.objects.get(id=pk)
    llamada.estado = "FINALIZADA"
    llamada.save()
    return redirect(reverse("clientes:detalles-cliente", args=[llamada.cliente.id]))

def rechazo_cliente(request, cliente_pk, interaccion_pk):
    cliente = Cliente.objects.get(id=cliente_pk)
    cliente.rechazos += 1
    llamada = Llamada.objects.get(id=interaccion_pk)
    #Una vez el cliente haya rechazado nuestras ofertas 3 veces, pasara a 
    #ser un cliente INACTIVO
    if cliente.rechazos < 3:
        fecha = date.today() + rd.relativedelta(days=15)
        Llamada.objects.create(fecha = fecha, cliente=cliente, observaciones=llamada.observaciones)
    else:
        cliente.estado = "INACTIVO"

    llamada.estado = "FINALIZADA"
    llamada.save()
    cliente.save()
    return redirect(reverse("clientes:detalles-cliente", args=[cliente.id]))

def reprogramar_visita(request, pk):
    visita = Visita.objects.get(id=pk)
    if request.method == "POST":
        carpeta_cliente = os.path.join(CARPETA_FUMIGACION, visita.cliente.nombre_orgnanizacion)
        src = os.path.join(carpeta_cliente, visita.fecha.strftime("%Y-%m-%d"))
        nueva_fecha = request.POST["nueva_fecha"]
        visita.fecha = nueva_fecha
        dst = os.path.join(carpeta_cliente, nueva_fecha)
        os.rename(src, dst)
        visita.save()
        
    return redirect(reverse("clientes:detalles-cliente", args=[visita.cliente.id]))

#def subir_archivo(request, cliente_pk, interaccion_pk):
#    visita = Visita.objects.get(id=interaccion_pk)
#    cliente = Cliente.objects.get(id=cliente_pk)
#    files = request.FILES.getlist("files")
#    path = f"{CARPETA_FUMIGACION}/{cliente.nombre_orgnanizacion}/{visita.fecha}"
#    write_file(files, path)
#    return redirect(reverse("clientes:detalles-cliente", args=[cliente.id]))
#
#    return redirect(f"/clientes/{cliente.id}")

#def eliminar_cliente(request, pk):
#    cliente = Cliente.objects.get(id=pk)
#    cliente.delete()
#    return redirect("/clientes")
#
#def crear_cliente(request):
#    form = ClienteModelForm
#    if request.method == "POST":
#        form = ClienteModelForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect("/clientes")
#
#    return render(request, "clientes/crear_cliente.html", {"form":form})
#
#def actualizar_cliente(request, pk):
#    cliente = Cliente.objects.get(id=pk)
#    form = ClienteModelForm(instance=cliente)
#    if request.method == "POST":
#        form = ClienteModelForm(request.POST, instance=cliente)
#        if form.is_valid():
#            form.save()
#            return redirect(f"/clientes/{pk}")
#
#    return render(request, "clientes/actualizar_cliente.html", {
    #        "cliente":cliente,
    #        "form":form
    #        })

#
#def lista_clientes(request):
#    clientes = Cliente.objects.all()
#    return render(request, "clientes/lista_clientes.html", {
    #        "clientes": clientes})
#




#We are using a fucntion based view for managing the deatils of our clientes, as it allow us 
#to easly create visits for certaing clients. 
#TODO: implement reverse instead of request
#def detalles_cliente(request, pk):
#    cliente = Cliente.objects.get(id=pk)
#    visitas = Visita.objects.filter(cliente_id=pk).order_by('-fecha')
#    form = VisitaForm
#    if request.method == "POST":
#        form = VisitaForm(request.POST)
#        if form.is_valid():
#            Visita.objects.create(
#                    fecha = form.cleaned_data["fecha"],
#                    observaciones = form.cleaned_data["observaciones"],
#                    cliente = cliente
#                    )
#            return redirect(f"/clientes/{pk}")
#
#
#    return render(request, "clientes/detalles_clientes.html", {
#           "cliente": cliente,
#           "visitas": visitas,
#           "form": form,
#           })


