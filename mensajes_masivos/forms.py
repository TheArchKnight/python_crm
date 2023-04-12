from django import forms
from django.http import request
from general_usage.models import *
from mensajes_masivos.models import Mensaje
dict_attrs = {"class":"form-control"}



class MensajeModelForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields=("lista_clientes",
                "contenido",
                "fecha_hora",
                )
        widgets={
                "lista_clientes":forms.Select(attrs=dict_attrs),
                "contenido":forms.Textarea(attrs=dict_attrs),
                "fecha_hora":forms.DateTimeInput(attrs={"type":"datetime-local"})
                }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["imagen_archivo"] = forms.FileField()

