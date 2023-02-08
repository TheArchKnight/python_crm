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
    path("<int:pk>/eliminar_visita/", VisitaDeleteView.as_view(), name="eliminar-visita")
#    path('<int:pk>/visitas/', include('visitas.urls', namespace='visitas'))
]
