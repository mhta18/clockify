from rest_framework import status
from rest_framework.response import Response
from authentication.permissions import IsUserAuthenticated
from .models import Notification
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
# Create your views here.


class NotificationMarkReadAPIView(APIView):


    permission_classes = [IsUserAuthenticated]

    def post(self, request, pk=None, *args, **kwargs):
        user_notifications = Notification.objects.filter(recipient=request.user)

        if pk is not None:
            notification = get_object_or_404(user_notifications, pk=pk)
            notification.is_read = True
            notification.save()
            return Response(
                {"detail": f"Notification {pk} marked as read."},
                status=status.HTTP_200_OK,
            )

        unread_count = user_notifications.filter(is_read=False).update(is_read=True)
        return Response(
            {"detail": f"Successfully marked {unread_count} notifications as read."},
            status=status.HTTP_200_OK,
        )
