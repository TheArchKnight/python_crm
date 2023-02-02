from django.shortcuts import render,redirect

from .models import *
from clientes.models import Cliente
from .forms import VisitaForm, VisitaModelForm
# Create your views here.


def agregar_visita(request, pk):
    cliente = Cliente.objects.get(id=pk)
    form = VisitaForm
    if request.method == "POST":
        form = VisitaForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            observaciones = form.cleaned_data['observaciones']
            Visita.objects.create(
                    fecha = fecha,
                    observaciones = observaciones,
                    cliente = cliente
                    )
            return redirect(f"/clientes/{pk}")

    return render(request, "visitas/agregar_visita.html", {
        "form":form,
        "cliente":cliente})

def editar_visita(request, pk):
    visita = Visita.objects.get(id=pk)
    print(pk)
    form = VisitaModelForm(instance=visita)
    if request.method == "POST":
        form = VisitaModelForm(request.POST, instance=visita)
        if form.is_valid():
            form.save()
            return redirect(f"/clientes/{visita.cliente.id}")
    return render(request, "visitas/editar_visita.html", {
        "form": form,
        "visita": visita,
        "cliente": visita.cliente
        })

def eliminar_visita(request, pk):
    visita = Visita.objects.get(id=pk)
    print(pk)
    id = visita.cliente.id
    visita.delete()
    return redirect(f"/clientes/{id}")
