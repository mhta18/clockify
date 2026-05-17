from django.shortcuts import render
from rest_framework import viewsets
from teams.models import Team
from teams.serializers import TeamSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
# Create your views here.
class TeamViewSet(viewsets.ModelViewSet):
 
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['name', 'created_at']

