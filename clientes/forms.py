from django import forms
from django.forms import PasswordInput, widgets
from .models import Cliente, Empleado, User, Visita
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, password_validation


class VisitaModelForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields=(
                'fecha',
                'observaciones',
#                "cliente",

                )
        widgets={
                "fecha" : forms.DateInput(attrs={"class": "form-control", "type": "date"}),
                "observaciones" : forms.Textarea(attrs={"class": "form-control"}),
#                "cliente": forms.Select(attrs={"class": "form-control"})
                }

class VisitaForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={"class":"form-control"}))
    observaciones = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "style":"resize:none"}))



class ClienteModelForm(forms.ModelForm):
    fields =()
    class Meta:
        model = Cliente
        fields = (
                'nombre_orgnanizacion',
                'direccion',
                'nit',
                'correo',
                'frecuencia_meses',
                )
        widgets = {
                'nombre_orgnanizacion': forms.TextInput(attrs={"class":'form-control'}),
                'direccion': forms.TextInput(attrs={"class":'form-control'}),
                'nit': forms.NumberInput(attrs={"class":'form-control'}),
                'correo': forms.EmailInput(attrs={"class":'form-control'}),
                'frecuencia_meses': forms.NumberInput(attrs={"class":'form-control'}),
#               'empleado': forms.Select(attrs={"class":'form-control'}),
                }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", 0)
        super(ClienteModelForm, self).__init__( *args, **kwargs)
        #Verify priviliges to assign clients to certain agents
        if user.is_organisor:
            queryset = Empleado.objects.all()
            choices = [[i,i] for i in queryset]
            choices.insert(0, ["---", "---"])
            self.fields["empleado_field"] = forms.ChoiceField(label="empleado", choices=choices)
              
            


#Deprecated in favor of ClienteModelForm
class ClienteForm(forms.Form):
    nombre_orgnanizacion = forms.CharField()
    direccion = forms.CharField()
    nit = forms.IntegerField()
    email = forms.EmailField()

class CustomUserNameField(UsernameField):
    def widget_attrs(self, widget):
        return {
                **super().widget_attrs(widget),
                "autocapitalize": "none",
                "autocomplete": "username",
                "class":"form-control",
                }


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Confirmar contraseña"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
        strip=False,
        help_text=(""),
    )
 
    class Meta:
        model = User
        fields=("username", "fumigacion", "fachadas", "inventario")
        field_classes = {"username": CustomUserNameField}
        labels = {
                "fumigacion": "Fumigacion",
                "fachadas": "Fachadas",
                "inventario": "Inventario",
                "username": "Nombre de usuario"
                }
        help_texts = {
                "username" : "",
                }

class LoginForm(AuthenticationForm):
    username = UsernameField(label=("Usuario"), widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control" }))
    password = forms.CharField(
            label=("Contraseña"),
            strip=False,
            widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control"}),
            )

