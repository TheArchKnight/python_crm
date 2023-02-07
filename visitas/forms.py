from django  import forms
from .models import Visita


class VisitaModelForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields=(
                'fecha',
                'observaciones',
#                "cliente",

                )
        widgets={
                "fecha" : forms.DateInput(attrs={"class": "form-control"}),
                "observaciones" : forms.Textarea(attrs={"class": "form-control"}),
#                "cliente": forms.Select(attrs={"class": "form-control"})
                }

class VisitaForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={"class":"form-control"}))
    observaciones = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "style":"resize:none"}))

