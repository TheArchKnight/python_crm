from django.urls import include, path
from fachadas.views import *
app_name="fachadas"


urlpatterns = [
    path('', ObraListView.as_view(), name="lista-obra"),
    path("iniciar-obra/", ObraCreateView.as_view(), name="iniciar-obra"),
    path("<int:obra_pk>/<str:año_mes>/<str:dia>", ObraDetailView.as_view(), name="detalles-obra"),
    path("eliminar-obra/<int:pk>", ObraDeleteView.as_view(), name="eliminar-obra"),
    path("<int:pk>/<str:año_mes>/<str:dia>/añadir-costo/", CostoCreateView.as_view(), name="crear-costo"),
    path("<int:pk>/<str:año_mes>/<str:dia>/añadir-trabajador", TrabajadorCreateView.as_view(), name="crear-trabajador"),
    path("<int:pk>/<str:año_mes>/<str:dia>/pagar_nomina", pagar_nomina, name="pagar-nomina")
    ]
