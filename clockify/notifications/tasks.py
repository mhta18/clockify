from celery import shared_task
from django.core.management import call_command
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task
def auto_clear_old_notifications():
    call_command("clear_old_notifications")


@shared_task
def send_background_notification_broadcast(
    recipient_id, notification_id, title, message
):

    channel_layer = get_channel_layer()
    if channel_layer is None:
        return "Channel Layer configuration missing or invalid"

    target_group = f"user_notifications_{recipient_id}"

    async_to_sync(channel_layer.group_send)(
        target_group,
        {
            "type": "send_notification",
            "notification": {
                "id": notification_id,
                "title": title,
                "message": message,
            },
        },
    )
    return f"Broadcast delivered successfully to group {target_group}"
