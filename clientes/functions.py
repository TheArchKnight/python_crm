from clientes.models import Interaccion


def unica_fecha(fecha):
    interacciones = Interaccion.objects.filter(fecha=fecha)
    if len(interacciones) > 0:
        return False
    return True

