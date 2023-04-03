from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from datetime import datetime

class Objeto(models.Model):

    #Generic relation https://docs.djangoproject.com/en/4.1/ref/contrib/contenttypes/#generic-relations
    #Points to the event from where the subelement is asked

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    ubicacion = GenericForeignKey('content_type', 'object_id')
    fecha = models.DateTimeField(default=datetime.today())
    usuario = models.ForeignKey("clientes.User", on_delete=models.SET_NULL, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
    def __str__(self):
        fecha =  self.fecha.strftime("%Y-%m-%d/%H:%M:%S")
        return f"{fecha}"

class Nota(Objeto):
    contenido = models.CharField(max_length=255)
    
class Pedido(models.Model):
    CHOICES_ESTADO = (("PEDIDO", "Pedido"), ("DESPACHADO", "DESPACHADO")) 

    estado = models.CharField(choices=CHOICES_ESTADO, max_length=30, default="PEDIDO")
    subelemento = models.ForeignKey("inventario.Subelemento", on_delete=models.CASCADE)
    elemento = models.ForeignKey("inventario.Elemento", on_delete=models.CASCADE)
    grupo_pedido = models.ForeignKey("general_usage.Grupo_Pedido", on_delete=models.CASCADE)

    cantidad_pedida = models.IntegerField(default=1)
    cantidad_enviada = models.IntegerField(default=0)

class Archivo(Objeto):
    nombre = models.CharField(max_length=255)

class Grupo_Pedido(Objeto):
    CHOICES_ESTADO = (("EN PROCESO", "En proceso"), ("FINALIZADO", "Finalizado")) 
    estado = models.CharField(choices=CHOICES_ESTADO, max_length=30, default="EN PROCESO")

