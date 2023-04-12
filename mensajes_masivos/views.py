from django.shortcuts import HttpResponseRedirect, render, reverse
from django.views.generic import CreateView, FormView, ListView
from functions import write_file
from general_usage.models import Archivo

from mensajes_masivos.forms import MensajeModelForm
from mensajes_masivos.models import Mensaje, CARPETA_MENSAJES
# Create your views here.

class MensajeCreateView(CreateView):
    template_name = "mensajes_masivos/crear_mensaje.html"
    form_class = MensajeModelForm
    id_archivo = 0

    def get_success_url(self):
        return reverse("mensajes_masivos:lista-mensajes")
    
    def post(self, request, **kwargs):
        form = MensajeModelForm(request.POST, request.FILES)
        if form.is_valid():
            path = CARPETA_MENSAJES + form.instance.lista_clientes + "/" + str(form.instance.fecha_hora) + "/"  
            file = write_file(request.FILES.getlist("imagen_archivo"), path=path, user=request.user)
            self.id_archivo = file.id
            return self.form_valid(form)

    def form_valid(self, form): 
        form.instance.imagen = Archivo.objects.get(id=self.id_archivo)
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"previous":reverse("mensajes_masivos:lista-mensajes")})
        return context

class MensajeListView(ListView):
    template_name = "mensajes_masivos/lista_mensajes.html"
    model = Mensaje
    context_object_name = "mensajes"

