from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'clientes'


router = DefaultRouter()
router.register(r'clientes-api', ClienteViewSet)
router.register(r'visitas', VisitaViewSet, basename='visitas')
router.register(r'llamadas', LlamadaViewSet)

