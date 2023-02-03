from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from visitas.forms import VisitaForm, VisitaModelForm

#from clientes.forms import ClienteForm
from .models import Cliente
from visitas.models import Visita
from .forms import ClienteModelForm

class LandingPageView(TemplateView):
    template_name = "landing.html"


class ClienteListView(ListView):
    template_name = "clientes/lista_clientes.html"
    queryset = Cliente.objects.all()
    context_object_name = "clientes"


#This view provides details of the client model, as well as 
#allows the user to create new visits. For this, a creatview class
#is used, and the context is updated with the necessary data for the forms
#and the details of data to work.
class ClienteDetailView(CreateView):
    template_name = "clientes/detalles_clientes.html"
    form_class= VisitaModelForm

    def get_success_url(self):
                                                    #Args receives a lits with arguments
        return reverse("clientes:detalles-cliente", args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        #Update the context with our necessary queries
        context.update({
            "visitas": Visita.objects.filter(cliente_id=self.kwargs["pk"]).order_by("-fecha"),
            "cliente":Cliente.objects.get(id=self.kwargs["pk"])
            })
        print(context)
        return context


class ClienteCreateView(CreateView):
    template_name = "clientes/crear_cliente.html"
    form_class=ClienteModelForm

    def get_success_url(self):
        return reverse("clientes:lista-cliente")


class ClienteUpdateView(UpdateView):
    template_name = "clientes/actualizar_cliente.html"
    queryset = Cliente.objects.all()
    form_class = ClienteModelForm

    def get_success_url(self):
        #The details-client function receives 2 arguments: request and the pk.
        return reverse("clientes:detalles-cliente", args=[self.kwargs['pk']])

class ClienteDeleteView(DeleteView):
    template_name = "clientes/eliminar_cliente.html"
    queryset = Cliente.objects.all()

    def get_success_url(self):
        return reverse("clientes:lista-cliente")




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
#def detalles_cliente(request, pk):
#
#    cliente = Cliente.objects.get(id=pk)
#    visitas = Visita.objects.filter(cliente_id=pk).order_by('-fecha')
#    form = VisitaModelForm
#    if request.method == "POST":
#        form = VisitaModelForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect(f"/clientes/{pk}")
#
#    return render(request, "clientes/detalles_clientes.html", {
#        "cliente": cliente,
#        "visitas": visitas,
#        "form": form,
#        })

