from datetime import date, datetime, timedelta
from crm_django.celery import app
from django.core.mail import send_mail
from clientes.models import Empleado, Cliente, Llamada, Visita
from fachadas.functions import *

@app.task
def visitas():
    empleados = Empleado.objects.all()
    for empleado in empleados:
        fecha = date.today()
        fecha_string = date.today().strftime("%Y-%m-%d")
        visitas = Visita.objects.filter(empleado=empleado, fecha=fecha)
        print(visitas)
        body_email = ''
        if len(visitas) > 0:
            body_email += f"Hola {empleado.user.username}\n"
            body_email += f"El dia de hoy, {len(visitas)} tienen una visita programada. Puedes visualizar mas a detalles en el CRM.\n\n"
            for visita in visitas:
                body_email += f"Nombre: {visita.cliente.nombre_orgnanizacion}\nDireccion: {visita.cliente.direccion}\nFrecuencia de visitas (meses): {visita.cliente.frecuencia_meses}\nObservaciones: {visita.observaciones}\n\n"
            print(body_email)
            send_mail(f"Visitas de fumigacion {fecha_string}", body_email, "settings.EMAIL_HOST_USER", [empleado.user.email], fail_silently=False)


@app.task
def llamadas():
    empleados =  Empleado.objects.all()
    for empleado in empleados:
        fecha = date.today()
        fecha_string = fecha.strftime("%Y-%m-%d")
        llamadas = Llamada.objects.filter(empleado = empleado, fecha=fecha)
        body_email=''
        if len(llamadas) > 0:
            body_email += f"¡Hola {empleado.user.username}!\n"
            body_email += f"El dia de hoy, {len(llamadas)} llamadas deben de ser realizadas. Puedes visualizar mas a detalles en el CRM.\n\n"
            for llamada in llamadas:
                visita = Visita.objects.filter(cliente = llamada.cliente).first() 
                body_email += f"Nombre: {llamada.cliente.nombre_orgnanizacion}\nDireccion: {llamada.cliente.direccion}\nFrecuencia de visitas (meses): {llamada.cliente.frecuencia_meses}\nUltima visita: {visita.fecha}\nMotivo de la llamada: {llamada.observaciones}\n\n"
            send_mail(f"Llamadas clientes {fecha_string}", body_email, "settings.EMAIL_HOST_USER", [empleado.user.email], fail_silently=False)


            









