from clientes.models import *
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        authentication_classes = [SessionAuthentication]
        permission_classes = [IsAuthenticated]


class InteraccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaccion
        fields = '__all__'
        authentication_classes = [SessionAuthentication]
        permission_classes = [IsAuthenticated]

class VisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = '__all__'
        authentication_classes = [SessionAuthentication]
        permission_classes = [IsAuthenticated]

class LlamadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Llamada
        fields = '__all__'
        authentication_classes = [SessionAuthentication]
        permission_classes = [IsAuthenticated]

