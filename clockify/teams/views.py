from django.shortcuts import render
from rest_framework import viewsets
from teams.models import Team
from teams.serializers import TeamSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Count
# Create your views here.
class TeamViewSet(viewsets.ModelViewSet):

    queryset = (
        Team.objects.all()
        .annotate(member_count=Count("member"))
        .prefetch_related("member")# reduce search timing and increase the speed of finding data. (n+1) 
    )
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ["created_at", "number_of_members"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "number_of_members", "name"]
