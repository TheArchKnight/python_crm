from django.urls import include, path
from inventario.views import *
app_name="inventario"

urlpatterns = [
    path('', ElementoListView.as_view(), name="lista-elementos"),
    path("crear_elemento", ElementoCreateView.as_view(), name="crear-elemento"),
    path("<int:elemento_pk>/", ElementoDetailView.as_view(), name="detalles-elemento"),
    path("eliminar/subelemento/<int:elem_pk>/<int:sub_pk>/", SubelementoDeleteView.as_view(), name="eliminar-subelemento"),
    path("editar/subelemento/<int:elem_pk>/<int:sub_pk>/", SubelementoUpdateView.as_view(), name="editar-subelemento"),
    path("eliminar/elemento/<int:elem_pk>/", ElementoDeleteView.as_view(), name="eliminar-elemento"),
    path("editar/elemento/<int:elem_pk>/", ElementoUpdateView.as_view(), name="editar-elemento")

    ]
