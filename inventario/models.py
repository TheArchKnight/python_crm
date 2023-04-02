from datetime import date
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.

class Elemento(models.Model):
    CHOCIES_CATEGORIA = (("HERRAMIENTA", "Herramienta"), ("INSUMO", "Insumo"))
    codigo_general = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=30)
    categoria = models.CharField(choices=CHOCIES_CATEGORIA, max_length=30)
    fecha = models.DateField(default=date.today())
    
    def __str__(self):
        return f"{self.codigo_general}-{self.descripcion}"
class Subelemento(models.Model):
    cantidad = models.IntegerField(default=1)
    codigo_unico = models.IntegerField()
    marca = models.CharField(max_length=30)
    elemento = models.ForeignKey("inventario.Elemento", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.codigo_unico} - {self.marca}"


