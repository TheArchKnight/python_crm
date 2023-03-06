from datetime import datetime
from crm_django.celery import app
from django.core.mail import send_mail
from clientes.models import Empleado, Cliente, Visita
@app.task
def send_notifications():
    queryset = Empleado.objects.all()
    for empleado in queryset:
        clientes_vencimiento = Cliente.objects.filter(fecha_vencimiento=datetime.today(), empleado = empleado, estado="ACTIVO")
        clientes_llamada = Cliente.objects.filter(fecha_llamada=datetime.today(), empleado=empleado, estado="ACTIVO")
        if len(clientes_vencimiento) > 0 or len(clientes_llamada) > 0:
            body_email = "¡Hola {empleado.user.username}!\n"
            for cliente in clientes_vencimiento:
                body_email += f"El dia de hoy, {len(clientes_vencimiento)} clientes han superado los terminos de tiempo con nuestros servicios. A continuacion encontraras algunos detalles de estos clientes, puedes visualizarlos mas a detalles en el CRM.\n\n"
    
                visita = Visita.objects.filter(cliente = cliente).first()
                body_email += f"Nombre: {cliente.nombre_orgnanizacion}\nDireccion: {cliente.direccion}\nFrecuencia de visitas (meses): {cliente.frecuencia_meses}\nUltima visita: {visita.fecha}\n\n"
            for cliente in clientes_llamada:
                body_email += f"El dia de hoy, {len(clientes_llamada)} deben de ser llamados para programar una proxima visita, ya que no accedieron al servicio una vez se habian vencido los terminos. A continuacion encontraras algunos detalles de estos clientes, puedes visualizarlos mas a detalles en el CRM.\n\n"
                visita = Visita.objects.filter(cliente = cliente).first()
                body_email += f"Nombre: {cliente.nombre_orgnanizacion}\nDireccion: {cliente.direccion}\nFrecuencia de visitas (meses): {cliente.frecuencia_meses}\nUltima visita: {visita.fecha}\nFecha de vencimiento: {cliente.fecha_vencimiento}\n"
            send_mail("Clientes con vencimiento de terminos", body_email, "settings.EMAIL_HOST_USER", [empleado.user.email], fail_silently=False)



