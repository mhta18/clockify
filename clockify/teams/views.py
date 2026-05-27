from django.shortcuts import render
from rest_framework import viewsets
from teams.models import Team
from teams.serializers import TeamSerializer
from users.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Count
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema_view,extend_schema

# Create your views here.

TEAM_UPLOAD_SCHEMA = {
    "multipart/form-data": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "The unique name of the team."},
            "description": {
                "type": "string",
                "description": "A brief overview of the team's department or focus.",
            },
            "logo": {
                "type": "string",
                "format": "binary",
                "description": "The team's profile image or avatar file.",
            },
            "supervisor": {
                "type": "integer", 
                "description": "The ID of the user assigned as the team's supervisor.",
                "nullable": False,
            },
            "members": {
                "type": "array",
                "items": {
                    "type": "integer",
                },
                "description": "A list of user UUIDs to add as members to this team.",
            },
        } 
    }
}


@extend_schema_view(
    create=extend_schema(request=TEAM_UPLOAD_SCHEMA),  # POST /teems/
    update=extend_schema(request=TEAM_UPLOAD_SCHEMA),  # PUT /teems/{id}/
    partial_update=extend_schema(request=TEAM_UPLOAD_SCHEMA),  # PATCH /teems/{id}/
)
class TeamViewSet(viewsets.ModelViewSet):

    queryset = (
        Team.objects.all()
        .annotate(member_count=Count("members"))
        .prefetch_related("members")# reduce search timing and increase the speed of finding data. (n+1) 
    )
    serializer_class = TeamSerializer
    permission_classes = [IsAdminUser]

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ["created_at"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "name"]

    parser_classes = (
        MultiPartParser,
        FormParser,
    )
