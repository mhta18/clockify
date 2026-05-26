from rest_framework import serializers
from .models import TimeLog
from projects.models import Project


class TimeLogSerializer(serializers.ModelSerializer):
    durration_seconds = serializers.SerializerMethodField()
    is_running = serializers.SerializerMethodField()

    class Meta:
        model = TimeLog
        fields = [
            "user",
            "project",
            "description",
            "start_time",
            "end_time",
            "duration_seconds",
            "is_running",
        ]
        read_only_fields = ["user" , "duration_seconds" , "is_running"]

    def get_duration_seconds(self,obj):
        return int(obj.duration.total_seconds())
    
    def get_is_running(self,obj):
        return obj.end_time is None
    
    def validate(self, attrs):
        user = self.context['request'].user

        instance = TimeLog(user=user,**attrs)

        try:
            instance.clean()
        except serializers.ValidationError as e:
            raise e
        except Exception as e:
            raise serializers.ValidationError(detail=str(e))
        

        return attrs