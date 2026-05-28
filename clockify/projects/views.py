from django.shortcuts import render
from rest_framework import viewsets, generics, mixins
from .serializers import ProjectSerializer
from .models import Project
from users.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema_view,extend_schema


PROJECT_SCHEMA = {
    "application/json": {
        "type": "object",
        "required": [
            "name"
        ], 
        "properties": {
            "name": {
                "type": "string",
                "maxLength": 100,
                "description": "The unique name of the project.",
            },
            "end_date": {
                "type": "string",
                "format": "date-time",
                "nullable": True,
                "description": "Optional deadline timestamp for the project closure.",
            },
            "color": {
                "type": "string",
                "maxLength": 7,
                "default": "#D1D5DB",
                "pattern": "^#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{6})$",
                "description": "Hex color code for UI themes. Must start with '#' (e.g., #FF5733).",
            },
            "teams": {
                "type": "array",
                "items": {
                    "type": "string",
                    "format": "uuid", 
                },
                "description": "A list of Team UUIDs associated with this project.",
            },
        },
    }
}

class ProjctListAPIView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser]


@extend_schema_view(
    create=extend_schema(
        request=PROJECT_SCHEMA,
        description="Create a brand new tracking project.",
    ),  # POST /projects/
    update=extend_schema(
        request=PROJECT_SCHEMA,
        description="Completely overwrite an existing project by its UUID.",
    ),  # PUT /projects/{id}/
    partial_update=extend_schema(
        request=PROJECT_SCHEMA,
        description="Partially alter optional properties of a project.",
    ),  # PATCH /projects/{id}/
)

class ProjctViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser]
