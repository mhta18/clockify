from django.shortcuts import render
from rest_framework import viewsets
from .models import Team, Task
from .serializers import TeamSerializer, TaskSerializer
from users.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Count
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.db import models
from .permissions import IsObjectWorkerOrSupervisor

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
        },
    }
}

TASK_SCHEMA = {
    "application/json": {
        "type": "object",
        "required": ["title", "team", "assigned_to", "deadline"],
        "properties": {
            "title": {
                "type": "string",
                "maxLength": 255,
                "description": "The title or heading of the task.",
            },
            "description": {
                "type": "string",
                "description": "Detailed text describing the task requirements or requirements breakdown.",
            },
            "team": {
                "type": "integer",
                "description": "The ID of the exact team this task belongs to.",
            },
            "assigned_to": {
                "type": "integer",
                "description": "The ID of the team member user being assigned to execute this task.",
            },
            "deadline": {
                "type": "string",
                "format": "date-time",
                "description": "The strict future deadline date and time for task completion (ISO 8601 format).",
            },
            "priority": {
                "type": "string",
                "enum": ["HIGH", "MEDIUM", "LOW"],
                "default": "MEDIUM",
                "description": "The severity priority categorization window of the task.",
            },
        },
    }
}


@extend_schema_view(
    create=extend_schema(request=TEAM_UPLOAD_SCHEMA),  # POST /teems/
    update=extend_schema(request=TEAM_UPLOAD_SCHEMA),  # PUT /teems/{id}/
    partial_update=extend_schema(request=TEAM_UPLOAD_SCHEMA),  # PATCH /teems/{id}/
)
class TeamViewSet(viewsets.ModelViewSet):

    serializer_class = TeamSerializer
    permission_classes = [IsAdminUser]

    queryset = (
        Team.objects.all()
        .annotate(member_count=Count("members"))
        .prefetch_related(
            "members"
        )  # reduce search timing and increase the speed of finding data. (n+1)
    )

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["created_at"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "name"]

    parser_classes = (
        MultiPartParser,
        FormParser,
    )


@extend_schema_view(
    create=extend_schema(
        summary="Create a new task",
        description="Allows a team's supervisor to create and assign tasks to workers within their exact team.",
        request=TASK_SCHEMA,
    ),
    update=extend_schema(
        summary="Replace an existing task",
        description="Completely updates a task instance. Restricted to the team's supervisor.",
        request=TASK_SCHEMA,
    ),
    partial_update=extend_schema(
        summary="Patch an existing task",
        description="Partially updates fields on a task. Restricted to the team's supervisor.",
        request=TASK_SCHEMA,
    ),
)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsObjectWorkerOrSupervisor]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_queryset(self):
        user = self.request.user

        if "supervisor" in self.request.path:
            return (
                Task.objects.filter(team__supervisor=user)
                .distinct()
                .order_by("deadline")
            )

        return Task.objects.filter(assigned_to=user).distinct().order_by("deadline")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
