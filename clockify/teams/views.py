from django.shortcuts import render
from rest_framework import viewsets
from teams.models import Team
from teams.serializers import TeamSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Count
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema_view,extend_schema

# Create your views here.

LOGO_SCHEMA = {
    "multipart/form-data": {
        "type": "object",
        "properties": {
            "logo": {
                "type": "string",
                "format": "binary",
            },
            "name": {"type": "string"},
            "description": {"type": "string"},
        },
    }
}


@extend_schema_view(
    create=extend_schema(request=LOGO_SCHEMA),  # POST /teems/
    update=extend_schema(request=LOGO_SCHEMA),  # PUT /teems/{id}/
    partial_update=extend_schema(request=LOGO_SCHEMA),  # PATCH /teems/{id}/
)
class TeamViewSet(viewsets.ModelViewSet):

    queryset = (
        Team.objects.all()
        .annotate(member_count=Count("members"))
        .prefetch_related("members")# reduce search timing and increase the speed of finding data. (n+1) 
    )
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ["created_at"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "name"]

    parser_classes = (
        MultiPartParser,
        FormParser,
    )
