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

    def validate_single_active_timer(self, user, request):
        http_method = request.method
        active_timer_exists = TimeLog.objects.filter(
            user=user, end_time__isnull=True
        ).first()

        if active_timer_exists:
            #START Workflow (POST /api/timelog/)
            if http_method == "POST" and "resume" not in request.path:
                raise serializers.ValidationError(
                    {
                        "non_field_errors": "You already have a running timer. Stop your current task first."
                    }
                )

            #RESUME Workflow (POST /api/timelog/{id}/res+ume/)
            elif http_method == "POST" and "resume" in request.path:
                raise serializers.ValidationError(
                    {
                        "non_field_errors": "Cannot resume. You have an active running timer right now."
                    }
                )

            #STOP / UPDATE Workflow (PUT or PATCH /api/timelog/{id}/)
            elif http_method in ["PUT", "PATCH"]:
                view = self.context.get("view")
                current_instance_id = view.kwargs.get("pk") if view else None

                # If they are patching a historical log while a timer is active, block them
                if current_instance_id and active_timer_exists.id != int(current_instance_id):
                    raise serializers.ValidationError(
                        {
                            "non_field_errors": "You cannot update past records while you have a running timer active."
                        }
                    )

    def validate(self, attrs):
        request = self.context.get('request')
        if not request:
            return attrs
            
        user = request.user
        self.validate_single_active_timer(user,request)

        instance = TimeLog(user=user,**attrs)

        try:
            instance.clean()
        except DjangoValidationError as e:
            raise e
        except Exception as e:
            raise serializers.ValidationError(detail=str(e))

        return attrs
