from datetime import datetime
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import AbstractUser

# Create your models here.

#User class for all of our users. The "type" of user, 
#is stablished by a forgein key from an instance of the diferent kind of users
#to this class
class User(AbstractUser):
    is_organisor = models.BooleanField(default=False)
    clientes = models.BooleanField(default=False)
    inventario = models.BooleanField(default=False)
    fachadas = models.BooleanField(default=False)
    mensajes = models.BooleanField(default=False)
    email = models.EmailField(null=False)

class Cliente(models.Model):

    CHOICES_ESTADO = (("INACTIVO", "Inactivo"), ("POTENCIAL", "Potencial"))
    CHOICES_SERVICIO = (("VENCIDO", "Vencido"), ("GARANTIA", "Garantia"), ("EN TERMINOS", "En terminos"))
    nombre_orgnanizacion = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255)
    apartamentos = models.CharField(max_length=50)
    nit = models.CharField(max_length=15)
    correo = models.EmailField(null=True)
    frecuencia_meses = models.IntegerField(default=1)
    empleado = models.ForeignKey("Empleado", on_delete=models.SET_NULL, null=True)
    fecha_vencimiento = models.DateField(null=True, default=None)
    administrador = models.CharField(max_length=150)
    supervisor = models.CharField(max_length=50)
    telefono_supervisor = models.CharField(max_length=30)
    correo_supervisor = models.EmailField()
    telefono = models.CharField(max_length=30)
    estado = models.CharField(max_length=20, choices = CHOICES_ESTADO)
    rechazos = models.IntegerField(default=0, null=False)
    estado_servicio = models.CharField(max_length=15, choices=CHOICES_SERVICIO)
    def __str__(self):
        return f"{self.nombre_orgnanizacion}"
  
class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

#class Visita(models.Model):
#    CHOICES_ESTADO = (("FINALIZADA", "Finalizada"), ("EN PROCESO", "En proceso"))
#
#    fecha = models.DateField()
#    observaciones = models.TextField()
#    cliente = models.ForeignKey("clientes.Cliente", on_delete=models.CASCADE)
#    estado = models.CharField(max_length=15, choices=CHOICES_ESTADO)
#    def __str__(self):
#        return f"{self.fecha}"

#class Llamada(models.Model):
#
#    CHOICES_ESTADO = (("REALIZADA", "Realizada"), ("PENDIENTE", "Pendiente"))
#    fecha = models.DateField()
#    cliente = models.ForeignKey("clientes.Cliente", on_delete=models.CASCADE)
#    observaciones = models.TextField()
#    estado = models.CharField(max_length=15, choices=CHOICES_ESTADO, default="PENDIENTE")

class Interaccion(models.Model):
    CHOICES_ESTADO = (("FINALIZADA", "Finalizada"), ("EN PROCESO", "En proceso"), ("PENDIENTE", "Pendiente"))
    fecha = models.DateField()
    fecha_creacion = models.DateField(auto_now_add=True)
    observaciones = models.CharField(max_length=255)
    cliente = models.ForeignKey("clientes.Cliente", on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=CHOICES_ESTADO, default="EN PROCESO")
    empleado = models.ForeignKey("clientes.Empleado", on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.fecha}"

class Visita(Interaccion):
    pass
class Llamada(Interaccion):
    def __init__(self, *args, **kwargs):
        super(Llamada, self).__init__(*args, **kwargs)
        if self.estado=="EN PROCESO":
            self.estado = "PENDIENTE"

#signal to execute when an user is created
def post_user_created_signal(sender, instance, created, **kwargs):
    if created and not instance.is_organisor:
      Empleado.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)

