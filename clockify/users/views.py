from django.shortcuts import render
from rest_framework import viewsets

from .models import User
from .permissions import IsAdminUser
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
