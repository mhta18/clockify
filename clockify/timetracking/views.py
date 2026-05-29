from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import TimeLogSerializer
from authentication.permissons import IsUserAuthenticated
from .models import TimeLog
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

# Create your views here.


class TimeLogViewSet(viewsets.ModelViewSet):
    serializer_class = TimeLogSerializer
    permission_classes = [IsUserAuthenticated]

    def get_queryset(self):
        return TimeLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        #validate that no running time exist
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"])
    def stop_current(self, request):
        running_timer = TimeLog.object.filter(user=request.user, end_time__isnull=True)

        if not running_timer:
            return Response(
                {"detail": "You do not have any active running timers right now."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        running_timer.end_time = timezone.now()
        running_timer.save()

        return Response(
            TimeLogSerializer(running_timer, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def resume(self, request, pk=None):
        # consider that there is an ID
        past_log = self.get_object()

        cloned_log = self.get_serializer(
            data={
                "project": past_log.project.id,
                "description": past_log.description,
                "start_time": timezone.now(),
            }
        )
        
        cloned_log.is_valid(raise_exception=True)
        cloned_log.save(user=request.user)

        return Response(cloned_log.data, status=status.HTTP_201_CREATED)
