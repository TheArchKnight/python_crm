from django.contrib import admin
from .models import User, Cliente, Empleado

# Register your models here.

admin.site.register(User)
admin.site.register(Cliente)
admin.site.register(Empleado)
