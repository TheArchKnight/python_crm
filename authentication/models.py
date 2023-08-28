from django.db import models
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


