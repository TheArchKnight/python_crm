


from django import forms
from django.forms import widgets
from .models import *

dict_widget = {"class":"form-control"}

class ElementoModelForm(forms.ModelForm):
    class Meta:
        model = Elemento
        fields = ("codigo_general",
                  "descripcion",
                  "categoria"
                )
        widgets = {"codigo_general": forms.NumberInput(attrs={"class": "form-control"}),
                   "descripcion": forms.TextInput(attrs={"class": "form-control"}),
                   "categoria": forms.Select(attrs={"class": "form-control"}),
                   }

class SubelementoModelForm(forms.ModelForm):
    class Meta:
        model = Subelemento
        fields = ("codigo_unico",
                  "marca",
                  "cantidad")
        widgets = {"codigo_unico": forms.NumberInput(attrs=dict_widget),
                   "marca": forms.TextInput(attrs=dict_widget),
                   "cantidad": forms.NumberInput(attrs=dict_widget)}


