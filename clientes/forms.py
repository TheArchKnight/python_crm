from datetime import date, datetime
from django import forms
from .models import Cliente, Empleado, Interaccion, User, Visita
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, password_validation
from datetime import timedelta


class InteraccionForm(forms.Form):
    TIPO = (("VISITA", "Visita"), ("LLAMADA", "Llamada"))
    tipo = forms.ChoiceField(widget = forms.Select(attrs={"class": "form-control"}), choices=TIPO)
    observaciones = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "style": "resize: none; height:150px"}))
    def __init__(self, *args, **kwargs):
        #We can only schedule new visits after the most recent one.
        ultima_visita = kwargs.pop("ultima_visita", 0)
        super(InteraccionForm, self).__init__( *args, **kwargs)
        dict = {"class": "form-control", "type": "date"} 
        
       # condicion = False
       # try:
       #     condicion =ultima_visita.fecha < date.today()
       # except:
       #     pass

       # if condicion or ultima_visita == None:
       # else:
        #    dict["min"] = (ultima_visita.fecha + timedelta(days=1)).strftime("%Y-%m-%d")
        dict["min"] = datetime.today().strftime("%Y-%m-%d")

        self.fields["fecha"] = forms.DateField(widget = forms.DateInput(attrs= dict)) 


class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = (
                'nombre_orgnanizacion',
                'direccion',
                'nit',
                "administrador",
                'telefono',
                'correo',
                'supervisor',
                'telefono_supervisor',
                'correo_supervisor',
                'frecuencia_meses',
                'apartamentos',
                "estado"
                )
        widgets = {
                'nombre_orgnanizacion': forms.TextInput(attrs={"class":'form-control'}),
                'direccion': forms.TextInput(attrs={"class":'form-control'}),
                'nit': forms.TextInput(attrs={"class":'form-control'}),
                'correo': forms.EmailInput(attrs={"class":'form-control'}),
                'frecuencia_meses': forms.NumberInput(attrs={"class":'form-control'}),
                "administrador":forms.TextInput(attrs={"class":'form-control'}),
                "telefono":forms.NumberInput(attrs={"class":'form-control'}),
                "estado": forms.Select(attrs={"class":"form-control"}),
                "supervisor": forms.TextInput(attrs={"class":"form-control"}),
                "telefono_supervisor": forms.TextInput(attrs={"class":"form-control"}),
                "correo_supervisor": forms.TextInput(attrs={"class":"form-control"}),
                'apartamentos': forms.TextInput(attrs={"class":'form-control'}),



                }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", 0)
        super().__init__( *args, **kwargs)
        
        #Verify priviliges to assign clients to certain agents
        if user.is_organisor:
            queryset = Empleado.objects.all()
            choices = [[i,i] for i in queryset]
            choices.insert(0, [None, "---"])
            self.fields["empleado_field"] = forms.ChoiceField(label="empleado", choices=choices)
        self.fields['correo'].required = False
        self.fields['correo_supervisor'].required = False

              
class ClienteModelFormUpdate(ClienteModelForm):
    class Meta:
        model = Cliente
        fields = (
                'nombre_orgnanizacion',
                'direccion',
                'nit',
                "administrador",
                'telefono',
                'correo',
                'supervisor',
                'telefono_supervisor',
                'correo_supervisor',
                'apartamentos',
                'frecuencia_meses',
                )
        widgets = {
                'nombre_orgnanizacion': forms.TextInput(attrs={"class":'form-control'}),
                'direccion': forms.TextInput(attrs={"class":'form-control'}),
                'nit': forms.TextInput(attrs={"class":'form-control'}),
                'correo': forms.EmailInput(attrs={"class":'form-control'}),
                'frecuencia_meses': forms.NumberInput(attrs={"class":'form-control'}),
                "administrador":forms.TextInput(attrs={"class":'form-control'}),
                "telefono":forms.NumberInput(attrs={"class":'form-control'}),
                "supervisor": forms.TextInput(attrs={"class":"form-control"}),
                "telefono_supervisor": forms.TextInput(attrs={"class":"form-control"}),
                "correo_supervisor": forms.TextInput(attrs={"class":"form-control"}),
                'apartamentos': forms.TextInput(attrs={"class":'form-control'}),

                }
        def __init__(self, *args, **kwargs):
            super().__init__( *args, **kwargs) 
            self.fields['correo'].required = False
            self.fields['correo_supervisor'].required = False



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
        fields=("username", "clientes", "email")
        field_classes = {"username": CustomUserNameField}
        labels = {
                "clientes": "Clientes",
                "fachadas": "Fachadas",
                "inventario": "Inventario",
                "username": "Nombre de usuario"
                }
        help_texts = {
                "username" : "",
                }
        widgets = {"email": forms.EmailInput(attrs={"class": "form-control"})}

class LoginForm(AuthenticationForm):
    username = UsernameField(label=("Usuario"), widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control" }))
    password = forms.CharField(
            label=("Contraseña"),
            strip=False,
            widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control"}),
            )
