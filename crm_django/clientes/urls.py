from django.urls import path
from clientes.views  import *
app_name = 'clientes'
urlpatterns = [
    path('', lista_clientes, name='lista-cliente'),
    path('<int:pk>/', detalles_clientes, name='detalles-cliente'),
    path('<int:pk>/actualizar/', actualizar_cliente, name='actualizar-cliente'),
    path('<int:pk>/eliminar/', eliminar_cliente, name='eliminar-cliente'),
    path('<int:pk>/agregar-visita/', agregar_visita, name='agregar-visita'),
    path('<int:pk>/editar_visita/', editar_visita, name='editar-visita' ),
    path('<int:pk>/eliminar_visita', eliminar_visita, name='eliminar-visita'),
    path('crear/', crear_cliente, name='crear-cliente')
]
