from django import forms
from clientes.models import Empleado

class EmpleadoModelForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = (
                "user",
                )
