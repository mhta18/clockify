from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def broadcast_notification(recipient, title, message):

    notification = Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
    )

    channel_layer = get_channel_layer()
    target_group = f"user_notifications_{recipient.id}"

    async_to_sync(channel_layer.group_send)(
        target_group,
        {
            "type": "send_notification",
            "notification": {
                "id": notification.id,
                "title": notification.title,
                "message": notification.message,
                "timestamp": notification.timestamp.isoformat(),
            },
        },
    )
