from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

class Cliente(models.Model):
    nombre_orgnanizacion = models.CharField(max_length=20)
    direccion = models.CharField(max_length=30)
    nit = models.IntegerField()
    administrador = models.CharField(max_length=25)
    correo = models.EmailField(null=True)
    observaciones = models.TextField()
    n_aptos = models.IntegerField(default=1)
    ultima_visita = models.DateField(null=True)
    proxima_visita = models.DateField(null=True)
    frecuencia_meses = models.IntegerField(default=1)
    
    empleado = models.ForeignKey("Empleado", on_delete=models.SET_NULL, null=True)
  
class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)






    
