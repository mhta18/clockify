from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = [
            "uuid",
            "name",
            "slug",
            "created_at",
            "end_date",
            "teams"
        ]
        read_only_fields =  ["uuid","slug","created_at"]