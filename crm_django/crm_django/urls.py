
from django.contrib import admin
from django.urls import include, path
urlpatterns = [
    path("admin/", admin.site.urls),
    path('clientes/', include('clientes.urls', namespace='clientes')),
    path("visitas/", include("visitas.urls", namespace="visitas"))
]
