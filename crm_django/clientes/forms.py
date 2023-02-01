from django import forms
from .models import Cliente, Visita

class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = (
                'nombre_orgnanizacion',
                'direccion',
                'nit',
                'correo',
                'frecuencia_meses',
                'empleado'
                )

class VisitaModelForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields=(
                'fecha',
                'observaciones'
                )

class VisitaForm(forms.Form):
    fecha = forms.DateField()
    observaciones = forms.CharField(widget=forms.Textarea)

#Deprecated in favor of ClienteModelForm
class ClienteForm(forms.Form):
    nombre_orgnanizacion = forms.CharField()
    direccion = forms.CharField()
    nit = forms.IntegerField()
    email = forms.EmailField()

