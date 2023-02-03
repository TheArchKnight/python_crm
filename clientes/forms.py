from django import forms
from .models import Cliente

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
        widgets = {
                'nombre_orgnanizacion': forms.TextInput(attrs={"class":'form-control'}),
                'direccion': forms.TextInput(attrs={"class":'form-control'}),
               'nit': forms.NumberInput(attrs={"class":'form-control'}),
                'correo': forms.EmailInput(attrs={"class":'form-control'}),
                'frecuencia_meses': forms.NumberInput(attrs={"class":'form-control'}),
                'empleado': forms.Select(attrs={"class":'form-control'}),
                }


#Deprecated in favor of ClienteModelForm
class ClienteForm(forms.Form):
    nombre_orgnanizacion = forms.CharField()
    direccion = forms.CharField()
    nit = forms.IntegerField()
    email = forms.EmailField()

