from re import I
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import request
from django.shortcuts import redirect, render


from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from clientes.mixins import EmpleadoRequiredMixin
from .forms import VisitaModelForm

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
    form_class= VisitaModelForm
    def get_success_url(self):
        #Args receives a list with arguments
        return reverse("clientes:detalles-cliente", args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        #Update the context with our necessary queries
        context.update({
            "visitas": Visita.objects.filter(cliente_id=self.kwargs["pk"]).order_by("-fecha"),
            "cliente":Cliente.objects.get(id=self.kwargs["pk"])
            }) 
        return context

    #Manually setting values for the form
    def form_valid(self, form):
        form.instance.cliente = Cliente.objects.get(id=self.kwargs["pk"])
        return super().form_valid(form)
        
class ClienteCreateView(EmpleadoRequiredMixin, CreateView):
    template_name = "clientes/crear_cliente.html"
    form_class=ClienteModelForm

    def get_success_url(self):
        return reverse("clientes:lista-cliente")
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        #TODO send email
        if self.request.user.is_organisor:
            empleado_username = form.cleaned_data["empleado_field"]
            form.instance.empleado = Empleado.objects.filter(user__username = empleado_username).first()
        else:
            form.instance.empleado = Empleado.objects.filter(user = self.request.user).first()
    
        return super(ClienteCreateView, self).form_valid(form)

class ClienteUpdateView(EmpleadoRequiredMixin, UpdateView):
    template_name = "clientes/actualizar_cliente.html"
    queryset = Cliente.objects.all()
    form_class = ClienteModelForm

    def get_success_url(self):
        #The details-client function receives 2 arguments: request and the pk.
        return reverse("clientes:detalles-cliente", args=[self.kwargs['pk']])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        #TODO send email
        if self.request.user.is_organisor:
            empleado_username = form.cleaned_data["empleado_field"]
            form.instance.empleado = Empleado.objects.filter(user__username = empleado_username).first()
        return super(ClienteUpdateView, self).form_valid(form) 


class ClienteDeleteView(EmpleadoRequiredMixin, DeleteView):
    template_name = "clientes/eliminar_cliente.html"
    queryset = Cliente.objects.all()

    def get_success_url(self):
        return reverse("clientes:lista-cliente")


class VisitaUpdateView(EmpleadoRequiredMixin, UpdateView):
    template_name = "visitas/editar_visita.html"
    queryset = Visita.objects.all()
    form_class = VisitaModelForm
    
    def get_context_data(self, **kwargs):
        context = super(VisitaUpdateView, self).get_context_data(**kwargs)
        #Update the context with our necessary queries
        context.update({
            "cliente":Cliente.objects.filter(visita = self.kwargs["pk"]).first()
            })        
        return context

    def get_success_url(self):
        return reverse("clientes:detalles-cliente", args=[Cliente.objects.filter(visita = self.kwargs["pk"]).first().id])


class VisitaDeleteView(EmpleadoRequiredMixin, DeleteView):
    template_name = "visitas/eliminar_visita.html"
    queryset = Visita.objects.all()
    
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


