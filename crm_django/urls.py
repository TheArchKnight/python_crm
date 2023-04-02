
from django.contrib import admin
from django.urls import include, path
from clientes.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from crm_django.settings import STATIC_ROOT, STATIC_URL

urlpatterns = [
    path("admin/", admin.site.urls),
    path('fumigacion/', include('clientes.urls', namespace='clientes')),
    #path("visitas/", include("visitas.urls", namespace="visitas")),
    path("empleados/", include("empleados.urls", namespace="empleados")),
    path("fachadas/", include('fachadas.urls', namespace='fachadas')),
    path("inventario/", include("inventario.urls", namespace="inventario")),
    path("creaciones_generales/", include("general_usage.urls", namespace="general_usage")),
    path("", LandingPageView.as_view(), name="landing-page" ),
    path("signup", SingupView.as_view(), name="signup"),
    path("logout", LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

