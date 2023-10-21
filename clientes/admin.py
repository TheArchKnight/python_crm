from django.contrib import admin
from .models import User, Cliente, Empleado, Visita

# Register your models here.

admin.site.register(User)
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Visita)
