from rest_framework import viewsets, generics,serializers,status
from .models import Team, Task
from rest_framework.response import Response
from .serializers import TeamSerializer, TaskSerializer,TaskMemberUpdateSerializer
from users.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    inline_serializer,
)
from .permissions import IsObjectWorkerOrSupervisor
from notifications.services import broadcast_notification

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
    "multipart/form-data": {
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


class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsObjectWorkerOrSupervisor]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_queryset(self):

        user = self.request.user
        return Task.objects.filter(assigned_to=user).distinct().order_by("deadline")


class TaskMemberUpdateAPIView(generics.UpdateAPIView):
    
    queryset = Task.objects.all()
    serializer_class = TaskMemberUpdateSerializer
    permission_classes = [IsObjectWorkerOrSupervisor]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assigned_to=user).distinct().order_by("deadline")

    def perform_update(self, serializer):
        original_task = Task.objects.get(pk=serializer.instance.pk)
        old_status = original_task.status        
        task = serializer.save()

        if old_status != task.status and task.status == Task.Status.DONE:
            supervisor = task.team.supervisor
            broadcast_notification(
                recipient=supervisor,
                title=task.title,
                message=f"Team member '{task.assigned_to.email}' has finished the task: '{task.title}'.",
            )


@extend_schema_view(
    create=extend_schema(
        summary="Create a new task",
        description="Allows a team's supervisor to create and assign tasks to workers within their exact team.",
        request=inline_serializer(
            name="TaskFormRequest",
            fields={
                "title": serializers.CharField(
                    max_length=255, help_text="The title of the task."
                ),
                "description": serializers.CharField(required=False),
                "team": serializers.ChoiceField(
                    choices=(
                        [(t.name) for t in Team.objects.all()]
                        if Team.objects.exists()
                        else []
                    ),
                    help_text="Select the target team for this assignment.",
                ),
                "assigned_to": serializers.IntegerField(
                    help_text="The ID of the team member user."
                ),
                "deadline": serializers.DateTimeField(
                    help_text="The strict future deadline (ISO 8601 format)."
                ),
                "priority": serializers.ChoiceField(
                    choices=["HIGH", "MEDIUM", "LOW"], default="MEDIUM"
                ),
            },
        ),
        responses={201: TaskSerializer},
    ),
    update=extend_schema(
        summary="Replace an existing task",
        description="Completely updates a task instance. Restricted to the team's supervisor.",
        request=TASK_SCHEMA,
    ),
    partial_update=extend_schema(
        request=TASK_SCHEMA,
    ),
)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsObjectWorkerOrSupervisor]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def create(self, request, *args, **kwargs):
        print("1. Enter Create View")
        data = request.data.copy()
        submitted_team_name = data.get("team")
        if submitted_team_name:
            team_instance = get_object_or_404(Team,name = submitted_team_name)
            data["team"] = str(team_instance.id)

        serializer = self.get_serializer(data=data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        print("2. Serializer is valid! Calling perform_create...")
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

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
        task = serializer.save(created_by=self.request.user)

        if task.assigned_to:
            broadcast_notification(
                recipient=task.assigned_to,
                title=task.title,
                message=f"You have been assigned a new task: '{task.title}' under team '{task.team.name}'.",
            )
