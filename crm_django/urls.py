from django.urls import include, path, re_path
from clientes.views import * 
from authentication.views import *
from clientes.urls import router as clientes_router 


urlpatterns = [
    path('', include(clientes_router.urls)),
    re_path('login-api', login),
    re_path('signup-api', signup),
]
