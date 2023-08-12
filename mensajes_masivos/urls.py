from django.urls import include, path
from general_usage.views import *
from mensajes_masivos.views import MensajeCreateView, MensajeListView
app_name="mensajes_masivos"

urlpatterns = [
        path("programar-mensaje", MensajeCreateView.as_view(), name="programar-mensaje"),
        path("lista-mensajes/", MensajeListView.as_view(), name="lista-mensajes")

        ]

