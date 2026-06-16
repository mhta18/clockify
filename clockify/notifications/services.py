import logging
from .models import Notification
from .tasks import send_background_notification_broadcast


def broadcast_notification(recipient, title, message):

    notification = Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
    )
    send_background_notification_broadcast.delay(
        recipient_id=recipient.id,
        notification_id=notification.id,
        title=notification.title,
        message=notification.message,
    )

    return notification
