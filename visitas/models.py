from django.db import models

# Create your models here.


class Visita(models.Model):
    fecha = models.DateField()
    observaciones = models.TextField()
    cliente = models.ForeignKey("clientes.Cliente", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.fecha}"


