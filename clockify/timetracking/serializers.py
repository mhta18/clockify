from django.core.exceptions import (
    ValidationError as DjangoValidationError,
)

from rest_framework import serializers
from .models import TimeLog


class TimeLogSerializer(serializers.ModelSerializer):
    duration_seconds = serializers.SerializerMethodField()

    class Meta:
        model = TimeLog
        fields = [
            "id",
            "user",
            "project",
            "description",
            "start_time",
            "end_time",
            "duration_seconds",
            "payment",
        ]
        read_only_fields = ["user", "duration_seconds"]

    def get_duration_seconds(self, obj):
        if obj.duration is None:
            return 0
        return int(obj.duration.total_seconds())

    def validate(self, attrs):
        request = self.context.get("request")
        if not request:
            return attrs

        user = request.user
        instance = TimeLog(user=user, **attrs)

        from rest_framework.exceptions import ValidationError as DRFValidationError

        try:
            instance.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(
                detail=e.message_dict if hasattr(e, "message_dict") else e.messages
            )
