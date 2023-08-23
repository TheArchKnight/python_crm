from datetime import datetime
from django import forms


from fachadas.models import *

class ObraModelForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ("nombre_obra",
                  "direccion",
                  "nit",
                  "administrador",
                  "correo",
                  "numero_tel",
                  "estado",
                  )
        widgets = {
                "nombre_obra" : forms.TextInput(attrs={"class": "form-control"}),
                "direccion" : forms.TextInput(attrs={"class": "form-control"}),
                "nit" : forms.NumberInput(attrs={"class":"form-control"}),
                "administrador": forms.TextInput(attrs={"class":"form-control"}),
                "correo" : forms.EmailInput(attrs={"class":"form-control"}),
                "estado" : forms.Select(attrs={"class":"form-control"}),
                "numero_tel":forms.NumberInput(attrs={"class":"form-control"})
                }

class CostoForm(forms.Form):
    dict = {"class":"form-control"}
    modelos = (("COSTO", "Costo"), ("ACCION", "Accion"))
    tipo = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control", "onchange":"select_form()"}), choices=modelos)
    descripcion = forms.CharField(widget = forms.TextInput(attrs=dict))
    cantidad = forms.IntegerField(widget = forms.NumberInput(attrs=dict))
    precio_unidad = forms.FloatField(widget=forms.NumberInput(attrs=dict)) 
    cobro_unidad = forms.FloatField(widget=forms.NumberInput(attrs=dict))

    def __init__(self, *args, **kwargs):
        obra = kwargs.pop("obra",0)
        trabajadores =  Trabajador.objects.filter(obra=obra)
        super(CostoForm, self).__init__( *args, **kwargs)
        dict_fecha = self.dict
        dict_fecha.update({"type": "date", "min": obra.fecha_inicio.strftime("%Y-%m-%d"), "max": date.today()})
        self.fields["fecha"] = forms.DateField(widget=forms.DateInput(attrs=dict_fecha))

        self.fields["trabajador"] = forms.ModelChoiceField(queryset=trabajadores, label="", empty_label="Seleccione el trabajador", widget=forms.Select(attrs={"class":"form-control", "style": "display:none;"}))
        self.fields["trabajador"].required = False

class TrabajadorModelForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ("nombre",
                  "cargo")
        widgets = {
                "nombre" : forms.TextInput(attrs={"class":"form-control"}),
                "cargo" : forms.Select(attrs={"class": "form-control"})
                }

