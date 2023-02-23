from datetime import datetime
from crm_django.celery import app
from django.core.mail import send_mail
from clientes.models import Empleado, Cliente, Visita
@app.task
def send_notifications():
    queryset = Empleado.objects.all()
    for empleado in queryset:
        clientes = Cliente.objects.filter(fecha_vencimiento=datetime.today(), empleado = empleado, estado="ACTIVO")
        for cliente in clientes:
            body_email = f"¡Hola {empleado.user.username}!\nEl dia de hoy, {len(clientes)} clientes han superado los terminos de tiempo con nuestros servicios. A continuacion encontraras algunos detalles de estos clientes, puedes visualizarlos mas a detalles en el CRM.\n\n"

            visita = Visita.objects.filter(cliente = cliente).first()
            body_email += f"Nombre: {cliente.nombre_orgnanizacion}\nDireccion: {cliente.direccion}\nFrecuencia de visitas (meses): {cliente.frecuencia_meses}\nUltima visita: {visita.fecha}\n\n"
            send_mail("Clientes con vencimiento de terminos", body_email, "settings.EMAIL_HOST_USER", [empleado.user.email], fail_silently=False)


