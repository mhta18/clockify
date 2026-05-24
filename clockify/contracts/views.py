from django.shortcuts import render
from .serializers import EmployerContractSerializer,FreelanserContractSerializer
from .models import FreelancerContract,EmployerContract
from rest_framework import generics,mixins
from users.permissions import IsAdminUser
# Create your views here.

class FreelancerListAPiView(generics.ListAPIView):
    queryset = FreelancerContract.objects.all()
    serializer_class = FreelanserContractSerializer
    permission_classes = [IsAdminUser]

class EmployerListAPIView(generics.ListAPIView):
    queryset = EmployerContract.objectsall()
    serializer_class = EmployerContractSerializer
    permission_classes = [IsAdminUser]

class FreelancerViewSet(mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    queryset = FreelancerContract.objects.all()
    serializer_class = FreelanserContractSerializer
    permission_classes = [IsAdminUser]    


class EmployerViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = EmployerContract.objects.all()
    serializer_class = EmployerContractSerializer
    permission_classes = [IsAdminUser]
