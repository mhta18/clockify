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

    
    def validate(self, attrs):
        request = self.context.get('request')
        if not request:
            return attrs
            
        user = request.user
        instance = TimeLog(user=user,**attrs)

        try:
            instance.clean()
        except DjangoValidationError as e:
            raise e
        except Exception as e:
            raise serializers.ValidationError(detail=str(e))

        return attrs
