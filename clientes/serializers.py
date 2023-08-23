from clientes.models import Cliente
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["nombre_orgnanizacion", "nit"]
        authentication_classes = [SessionAuthentication]
        permission_classes = [IsAuthenticated]
