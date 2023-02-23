from django.contrib import admin
from .models import User, Cliente, Empleado, UserProfile, Visita

# Register your models here.

admin.site.register(User)
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(UserProfile)
admin.site.register(Visita)
