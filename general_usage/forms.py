from django import forms
from django.http import request
from general_usage.models import *
from inventario.models import Elemento, Subelemento
dict_attrs = {"class":"form-control"}

class PedidoModelForm(forms.ModelForm):
    elemento = forms.ModelChoiceField(queryset=Elemento.objects.all(), widget=forms.Select(attrs={"class":"form-control"}))

    class Meta:
        model = Pedido
        fields = (
                "elemento",
                "subelemento",
                "cantidad_pedida",
                )
        widgets={
                "subelemento": forms.Select(attrs=dict_attrs),
                "cantidad_pedida": forms.NumberInput(attrs=dict_attrs)
                }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subelemento"].queryset = Subelemento.objects.none()
        if 'elemento' in self.data:
            try:
                elemento_id = int(self.data.get('elemento'))
                self.fields['subelemento'].queryset = Subelemento.objects.filter(elemento_id=elemento_id).order_by('codigo_unico')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk:
            self.fields['subelemento'].queryset = self.instance.elemento.subelemento_set.order_by('codigo_unico')

PedidoFormSetUpdate = forms.modelformset_factory(model=Pedido,fields=('cantidad_pedida', 'elemento', 'subelemento','cantidad_enviada'), 
                                           widgets={"cantidad_pedida": forms.NumberInput(attrs=dict_attrs),
                                                    "elemento": forms.Select(attrs=dict_attrs),
                                                    "subelemento":forms.Select(attrs=dict_attrs)

                                                    })

PedidoFormSetCreate = forms.modelformset_factory(model=Pedido,fields=('cantidad_pedida', 'elemento', 'subelemento'), 

                                           widgets={"cantidad_pedida": forms.NumberInput(attrs=dict_attrs),
                                                    "elemento": forms.Select(attrs=dict_attrs),
                                                    "subelemento":forms.Select(attrs=dict_attrs)

                                                    })

