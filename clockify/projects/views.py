from django.shortcuts import render
from rest_framework import viewsets, generics, mixins
from .serializers import ProjectSerializer
from .models import Project
from users.permissions import IsAdminUser

# Create your views here.


class ProjctListAPIView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser]


class ProjctViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser]
