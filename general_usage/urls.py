from django.urls import include, path
from general_usage.views import *
app_name="general_usage"


urlpatterns=[
        path("crear_nota/<str:tipo>/<int:pk>/", NotaCreateView.as_view(), name="crear-nota"),
        path("subir_archivo/<str:tipo>/<int:pk>/", ArchivoCreateView.as_view(), name="subir-archivo"),
        path("crear-pedido/<str:tipo>/<str:fecha>/<int:pk>/", PedidoFormsetView.as_view(), name="crear-pedido"),
        path('ajax/cargar_subelementos', cargar_subelementos, name='ajax_cargar_subelementos'), # AJAX
        ]

