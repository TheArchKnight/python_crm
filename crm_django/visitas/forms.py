from django  import forms
from .models import Visita


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

