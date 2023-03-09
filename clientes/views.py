from datetime import date, timedelta
from dateutil import relativedelta as rd

from django.contrib.auth.views import LoginView, reverse_lazy
#from django.http import HttpResponseForbidden, request
from django.shortcuts import redirect, render


from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from clientes.mixins import EmpleadoRequiredMixin
from .forms import InteraccionModelForm

#from clientes.forms import ClienteForm
from .models import Cliente, Empleado
from .models import Visita
from .forms import ClienteModelForm, CustomUserCreationForm, LoginForm


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
            if request.user.inventario and not (request.user.fachadas or request.user.fumigacion):
                return redirect("inventario:lista")
            else:
                return redirect("clientes:lista-cliente")
        return super(LandingPageView, self).get(request, *args, **kwargs)



class ClienteListView( EmpleadoRequiredMixin ,ListView):
    template_name = "clientes/lista_clientes.html"
    context_object_name = "clientes"
    

    #Queryset for the clients assigned to the user.
    #Users with only acces to the inventory are not allowed
    #to review clients information
    def get_queryset(self):
        queryset = Cliente.objects.all()
        if self.request.user.fachadas or self.request.user.fumigacion:
            queryset = queryset.filter(empleado__user=self.request.user)
        return queryset



#This view provides details of the client model, as well as 
#allows the user to create new visits. For this, a creatview class
#is used, and the context is updated with the necessary data for the forms
#and the details of data to work.
class ClienteDetailView(EmpleadoRequiredMixin, CreateView):
    template_name = "clientes/detalles_clientes.html"
    form_class= InteraccionModelForm
    def get_success_url(self):
        #Args receives a list with arguments
        return reverse("clientes:detalles-cliente", args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        #visitas = Visita.objects.filter(cliente_id=self.kwargs["pk"]).order_by("-fecha")
        #Update the context with our necessary queries
        context.update({
            "visitas": Visita.objects.filter(cliente_id=self.kwargs["pk"]).order_by("-fecha"),
            "cliente":Cliente.objects.get(id=self.kwargs["pk"])
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
        form.instance.cliente = cliente
        visitas = Visita.objects.filter(cliente_id=self.kwargs["pk"]).order_by("-fecha")
        #set default values for client once a service is scheduled
        if visitas.count() == 0:
            cliente.estado = "ACTIVO"
        cliente.rechazos = 0
        cliente.save()
        form.instance.estado = "EN PROCESO"

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

    def form_valid(self, form):
        #Allow organisor users to assing clients to agents.
        if self.request.user.is_organisor:
            empleado_username = form.cleaned_data["empleado_field"]
            form.instance.empleado = Empleado.objects.get(user__username = empleado_username)
        else:
            form.instance.empleado = Empleado.objects.get(user = self.request.user)
    
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

    def form_valid(self, form):
        #TODO send email
        if self.request.user.is_organisor:
            empleado_username = form.cleaned_data["empleado_field"]
            form.instance.empleado = Empleado.objects.get(user__username = empleado_username)
        return super(ClienteUpdateView, self).form_valid(form) 


class ClienteDeleteView(EmpleadoRequiredMixin, DeleteView):

    model = Cliente
    http_method_names = ['delete']

    def dispatch(self, request, *args, **kwargs):
        handler = getattr(self, 'delete')
        return handler(request, *args, **kwargs)

    def get_success_url(self):
        success_url = str(reverse_lazy('clientes:lista-cliente'))
        return success_url


class VisitaUpdateView(EmpleadoRequiredMixin, UpdateView):
    template_name = "visitas/editar_visita.html"
    queryset = Visita.objects.all()
    form_class = InteraccionModelForm

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

def search_clientes(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        clientes = Cliente.objects.filter(nombre_orgnanizacion__icontains=searched)
        return render(request, "search_clientes.html", {"searched": searched, "clientes": clientes})
    else:
        return render(request, "search_clientes.html", {})

def finalizar_visita(request, pk):
    visita = Visita.objects.get(id=pk)
    visita.estado = "FINALIZADA"
    visita.save()
    cliente = Cliente.objects.get(visita__id=pk)
    cliente.fecha_vencimiento = visita.fecha + rd.relativedelta(months=cliente.frecuencia_meses)
    if cliente.fecha_vencimiento.weekday() > 4:
        cliente.fecha_vencimiento += timedelta(days=7-cliente.fecha_vencimiento.weekday())
    cliente.save()
    return redirect(f"/clientes/{cliente.id}")

def rechazo_cliente(request, pk):
    cliente = Cliente.objects.get(id=pk)
    cliente.rechazos += 1
    #Una vez el cliente haya rechazado nuestras ofertas 3 veces, pasara a 
    #ser un cliente INACTIVO
    if cliente.rechazos == 3:
        cliente.estado = "INACTIVO"
    else:
        cliente.fecha_llamada = date.today() + rd.relativedelta(days=15)
    cliente.save()
    return redirect(f"/clientes/{cliente.id}")


def reprogramar_visita(request, pk):
    visita = Visita.objects.get(id=pk)
    if request.method == "POST":
        nueva_fecha = request.POST["nueva_fecha"]
        visita.fecha = nueva_fecha
        visita.save()
    return redirect(f"/clientes/{visita.cliente.id}")


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


