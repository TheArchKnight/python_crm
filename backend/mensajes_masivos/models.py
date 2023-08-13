from time import sleep
from django.db import models
from django.db.models.base import post_save
from django.dispatch import receiver
from clientes.models import Cliente
from crm_django.celery import app

from alright import WhatsApp

# Create your models here.
CARPETA_MENSAJES = "/home/anorak/Test/Mensajes/" 

class Mensaje(models.Model):
    CHOICES_LISTA = (("INACTIVO", "Inactivo"), ("ACTIVO", "Activo"), ("POTENCIAL", "Potencial"), ("TODOS", "Todos"))
    contenido = models.TextField()
    lista_clientes = models.CharField(max_length=30, choices=CHOICES_LISTA)
    fecha_hora = models.DateTimeField(null=False)
    imagen = models.ForeignKey("general_usage.Archivo", on_delete=models.CASCADE, null=True, default=None)
    estado = models.CharField(max_length=30, default="PENDIENTE")

@app.task
def enviar_mensaje(id):
    messenger = WhatsApp()
    mensaje = Mensaje.objects.get(id=id)
    clientes = Cliente.objects.all()
    if mensaje.lista_clientes != "TODOS":
        clientes = clientes.filter(estado=mensaje.lista_clientes) 
    for cliente in clientes:
        messenger.find_user('57'+str(cliente.telefono)) 
        messenger.send_message(mensaje.contenido)
        sleep(5)
    mensaje.estado = "ENVIADO"
    mensaje.save()

@receiver(post_save, sender=Mensaje)
def programar_mensaje(sender, instance, created, **kwargs):
    if created:        
        enviar_mensaje.apply_async(args=[instance.id], eta=instance.fecha_hora)



