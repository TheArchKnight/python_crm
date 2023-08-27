
from django.contrib import admin
from django.urls import include, path, re_path
from clientes.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView


from authentication.views import *
urlpatterns = [
    path("admin/", admin.site.urls),
    path('Clientes/', include('clientes.urls', namespace='clientes')),
    #path("visitas/", include("visitas.urls", namespace="visitas")),
    path("empleados/", include("empleados.urls", namespace="empleados")),
    path("fachadas/", include('fachadas.urls', namespace='fachadas')),
    path("inventario/", include("inventario.urls", namespace="inventario")),
    path("creaciones_generales/", include("general_usage.urls", namespace="general_usage")),
#    path("mensajes_masivos/", include("mensajes_masivos.urls", namespace="mensajes_masivos")),
    path("", LandingPageView.as_view(), name="landing-page" ),
    path("signup", SingupView.as_view(), name="signup"),
    path("logout", LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#Django rest urls


from rest_framework import routers
from clientes import views

router = routers.DefaultRouter()
router.register(r'clientes-api', views.ClienteViewSet)

urlpatterns += [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path('login-api', login),
    re_path('signup-api', signup),
]
