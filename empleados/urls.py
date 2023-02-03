from django.urls import path
from .views import *
app_name="empleados"

urlpatterns=[
    path("", EmpleadoListView.as_view(), name="lista-empleados"),
    path("crear/", EmpleadoCreateView.as_view(), name="crear-empleado"),
    path('<int:pk>/', EmpleadoDetailView.as_view(), name='detalles-empleado'),
    path('<int:pk>/actualizar/',EmpleadoUpdateView.as_view(), name='editar-empleado'),
    path('<int:pk>/eliminar/', EmpleadoDeleteView.as_view(), name='eliminar-empleado'),


        ]
