from django.shortcuts import render
from rest_framework import viewsets
from teams.models import Team
from teams.serializers import TeamSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class TeamViewSet(viewsets.ModelViewSet):
 
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

