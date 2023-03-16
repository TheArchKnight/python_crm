from django.urls import include, path
from clientes.views  import *
app_name = 'clientes'
urlpatterns = [
    path('', ClienteListView.as_view(), name='lista-cliente'),
    path('<int:pk>/', ClienteDetailView.as_view(), name='detalles-cliente'),
    path('<int:pk>/actualizar/', ClienteUpdateView.as_view(), name='actualizar-cliente'),
    path('<int:pk>/eliminar/', ClienteDeleteView.as_view(), name='eliminar-cliente'),
    path('crear/', ClienteCreateView.as_view(), name='crear-cliente'),
    path("<int:pk>/editar/", VisitaUpdateView.as_view(), name="editar-visita"),
    path("<int:pk>/eliminar_visita/", VisitaDeleteView.as_view(), name="eliminar-visita"),
    path("<int:pk>/finalizar_visita/", finalizar_visita, name="finalizar-visita"),
    path("<int:cliente_pk>/<int:interaccion_pk>/rechazo/", rechazo_cliente, name="rechazo"),
    path("busqueda/", search_clientes, name="search-clientes" ),
    path("<int:pk>/reprogramar/", reprogramar_visita, name="reprogramar-visita"),
    path("<int:cliente_pk>/<int:interaccion_pk>/subir_archivo",subir_archivo, name="subir-archivo"),
    path("<int:pk>/finalizar_llamada/", finalizar_llamada, name="finalizar-llamada")
#    path('<int:pk>/visitas/', include('visitas.urls', namespace='visitas'))
]
