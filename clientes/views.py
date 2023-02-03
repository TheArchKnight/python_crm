from django.shortcuts import redirect, render

from visitas.forms import VisitaForm, VisitaModelForm

#from clientes.forms import ClienteForm
from .models import Cliente
from visitas.models import Visita
from .forms import ClienteModelForm
def landing(request):
    return render(request, "landing.html")

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "clientes/lista_clientes.html", {
        "clientes": clientes})

def detalles_clientes(request, pk):

    cliente = Cliente.objects.get(id=pk)
    visitas = Visita.objects.filter(cliente_id=pk).order_by('-fecha')
    form = VisitaModelForm
    if request.method == "POST":
        form = VisitaModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"/clientes/{pk}")

    return render(request, "clientes/detalles_clientes.html", {
        "cliente": cliente,
        "visitas": visitas,
        "form": form,
        })


def crear_cliente(request):
    form = ClienteModelForm
    if request.method == "POST":
        form = ClienteModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/clientes")

    return render(request, "clientes/crear_cliente.html", {"form":form})


def actualizar_cliente(request, pk):
    cliente = Cliente.objects.get(id=pk)
    form = ClienteModelForm(instance=cliente)
    if request.method == "POST":
        form = ClienteModelForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect(f"/clientes/{pk}")

    return render(request, "clientes/actualizar_cliente.html", {
        "cliente":cliente,
        "form":form
        })

def eliminar_cliente(request, pk):
    cliente = Cliente.objects.get(id=pk)
    cliente.delete()
    return redirect("/clientes")


