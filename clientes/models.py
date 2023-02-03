from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username


class Cliente(models.Model):
    nombre_orgnanizacion = models.CharField(max_length=20)
    direccion = models.CharField(max_length=30)
    nit = models.IntegerField()
    correo = models.EmailField(null=True)
    frecuencia_meses = models.IntegerField(default=1)
    empleado = models.ForeignKey("Empleado", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre_orgnanizacion}"
  
class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username




   
