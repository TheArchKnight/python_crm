from django.urls import include, path
from clientes.views  import *
app_name = 'clientes'
urlpatterns = [
    path('', lista_clientes, name='lista-cliente'),
    path('<int:pk>/', detalles_clientes, name='detalles-cliente'),
    path('<int:pk>/actualizar/', actualizar_cliente, name='actualizar-cliente'),
    path('<int:pk>/eliminar/', eliminar_cliente, name='eliminar-cliente'),
    path('crear/', crear_cliente, name='crear-cliente'),
    path('<int:pk>/visitas/', include('visitas.urls', namespace='visitas'))
]
