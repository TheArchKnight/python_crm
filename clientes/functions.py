from clientes.models import *

def definir_tipos(interaccion):
    if isinstance(interaccion, Visita):
        return "Visita"
    elif isinstance(interaccion, Llamada):
        return "Llamada"
 
