from datetime import date
from django.db import models

class Obra(models.Model):

    CHOICES_ESTADO = (("EN PROCESO", "En proceso"), ("FINALIZADA", "Finalizada"))

    nombre_obra = models.CharField(max_length=30)
    direccion = models.CharField(max_length=30)
    nit = models.IntegerField()
    administrador = models.CharField(max_length=30)
    numero_tel = models.IntegerField()
    correo = models.EmailField(null=True)
    empleado = models.ForeignKey("clientes.Empleado", on_delete=models.SET_NULL, null=True)
    estado = models.CharField(max_length=10, choices = CHOICES_ESTADO)
    fecha_inicio = models.DateField(null=False, default=date.today)
    costo_total = models.FloatField(default=0)
    fecha_ultimo_pago = models.CharField(max_length=25, default=0)

    def __str__(self):
        return f"{self.nombre_obra}"


class Costo(models.Model):
    descripcion = models.CharField(max_length=30)
    cantidad = models.IntegerField()
    fecha = models.DateField(null=False, default=date.today)
    obra = models.ForeignKey("fachadas.Obra", on_delete=models.CASCADE)
    precio_unidad = models.FloatField()
    cobro_unidad = models.FloatField()

    def __str__(self):
        return f"{self.descripcion}"

class Accion(Costo):
    trabajador = models.ForeignKey("fachadas.Trabajador", on_delete=models.SET_NULL, null=True)

class Trabajador(models.Model):
    CHOICES_TIPO = (("SUPERVISOR", "Supervisor"), ("OBRERO", "Obrero"))
    nombre = models.CharField(max_length=30)
    cargo = models.CharField(max_length=30,choices = CHOICES_TIPO)
    obra = models.ForeignKey("fachadas.Obra", on_delete=models.SET_NULL, null=True)
    acumulado = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.nombre}"

class Pago(models.Model):
    fecha = models.DateField(null=False)
    periodo_inicio = models.DateField()
    periodo_final = models.DateField()
    monto = models.FloatField()
    trabajador = models.ForeignKey("fachadas.Trabajador", on_delete=models.CASCADE, null=False)
    obra = models.ForeignKey("fachadas.Obra", on_delete=models.CASCADE, null=False)
    def __str__(self):
        return f"{self.monto}"

