from django import forms
from django.forms import PasswordInput, widgets
from .models import Cliente, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, password_validation


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
        fields=("username", "is_agent")
        field_classes = {"username": CustomUserNameField}
        labels = {
                "is_agent": "Empleado",
                "username": "Nombre de usuario"
                }
        help_texts = {
                "username" : "",
                "password1": ""
                }

class LoginForm(AuthenticationForm):
    username = UsernameField(label=("Usuario"), widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control" }))
    password = forms.CharField(
            label=("Contraseña"),
            strip=False,
            widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control"}),
            )

