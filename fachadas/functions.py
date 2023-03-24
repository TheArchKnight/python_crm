from datetime import datetime
from fachadas.models import *

def acumulado_trabajador(trabajadores):
    acumulados = []
    for trabajador in trabajadores:
        acciones = Accion.objects.filter(trabajador=trabajador)
        acumulados.append(sum(map(lambda x: x.precio_unidad, acciones)))
    return acumulados

def asignar_acciones(costos,obra,fecha):
    costos_list = list(costos).copy()
    acciones_id = [i.id for i in Accion.objects.filter(obra=obra, fecha=fecha)]
    for i in range(len(costos_list)):
        if costos_list[i].id in acciones_id:
            costos_list[i] = Accion.objects.get(id=costos_list[i].id)
    return costos_list

def unir_fecha(kwargs):
    año_mes = kwargs["año_mes"]
    dia = kwargs["dia"]
    fecha = f"{año_mes}-{dia}"
    return {"fecha":datetime.strptime(fecha, "%Y-%m-%d").date(), 
            "año_mes":año_mes, 
            "dia": dia}

def valores_unicos(lista):
    lista1 = []
    for elemento in lista:
        if elemento not in lista1:
            lista1.append(elemento)
    return lista1

