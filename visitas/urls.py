from django.urls import path
from clientes.views  import *
from visitas.views import *
app_name = 'visitas'
urlpatterns = [
        path('<int:pk>/agregar_visita', agregar_visita, name='agregar-visita'),
        path('<int:pk>/editar_visita', editar_visita, name='editar-visita'),
        path('<int:pk>/eliminar_visita', eliminar_visita, name='eliminar-visita')
        ]

