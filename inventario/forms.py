


from django import forms
from django.forms import widgets
from .models import *

class ConsumableModelForm(forms.ModelForm):
    class Meta:
        model = Consumable
        exclude = ("visit")
        widgets = {"code": forms.NumberInput(attrs={"class": "form-class"}),
                   "quantity": forms.NumberInput(attrs={"class": "form-class"}),
                   "description": forms.Textarea(attrs={"class": "form-class"}),
                   }

class ToolModelForm(forms.ModelForm):
    class Meta:
        model = Tool
        exclude = ("visit")
        widgets = {"code": forms.NumberInput(attrs={"class": "form-class"}),
                   "description": forms.Textarea(attrs={"class": "form-class"}),
                   }



