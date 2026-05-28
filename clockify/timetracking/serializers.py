from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import TimeLog
from projects.models import Project


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
        read_only_fields = ["user" , "duration_seconds"]

    def get_duration_seconds(self,obj):
        if obj.duration is None:
            return 0
        return int(obj.duration.total_seconds())

    def validate_single_active_timer(self, user):
        active_timer_exists = TimeLog.objects.filter(
            user=user, end_time__isnull=True
        ).exists()

        if active_timer_exists:
            raise serializers.ValidationError(
                {
                    "non_field_errors": "You already have a running timer. Stop your current task first."
                }
            )

    def validate(self, attrs):
        user = self.context['request'].user
        self.validate_single_active_timer(user)

        instance = TimeLog(user=user,**attrs)

        try:
            instance.clean()
        except DjangoValidationError as e:
            raise e
        except Exception as e:
            raise serializers.ValidationError(detail=str(e))

        return attrs
