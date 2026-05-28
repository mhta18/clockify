from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "slug",
            "created_at",
            "end_date",
            "teams",
            "color"
        ]
        read_only_fields =  ["id","slug","created_at"]

    def validate_color(self, value):
        if value and not value.startswith("#"):
            raise serializers.ValidationError(
                "Color must be a valid hex code starting with '#'."
            )
        return value
