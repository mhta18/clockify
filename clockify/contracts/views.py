from django.shortcuts import render
from .serializers import EmployerContractSerializer, FreelanserContractSerializer
from .models import FreelancerContract, EmployerContract
from rest_framework import generics, mixins,viewsets
from users.permissions import IsAdminUser

# Create your views here.


class FreelancerContractListAPiView(generics.ListAPIView):
    queryset = FreelancerContract.objects.all()
    serializer_class = FreelanserContractSerializer
    permission_classes = [IsAdminUser]


class EmployerContractListAPIView(generics.ListAPIView):
    queryset = EmployerContract.objects.all()
    serializer_class = EmployerContractSerializer
    permission_classes = [IsAdminUser]


class FreelancerContractViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = FreelancerContract.objects.all()
    serializer_class = FreelanserContractSerializer
    permission_classes = [IsAdminUser]


class EmployerContractViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = EmployerContract.objects.all()
    serializer_class = EmployerContractSerializer
    permission_classes = [IsAdminUser]
