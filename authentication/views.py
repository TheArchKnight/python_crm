from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from authentication.models import User
from django.shortcuts import get_object_or_404
from clientes.models import Empleado

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data["password"]):
        return Response({"detail": "Not found."}, status=status.status.HTTP_404_NOT_FOUND)
    token = Token.objects.get(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user":serializer.data})


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        Empleado.objects.create(user=user)
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


