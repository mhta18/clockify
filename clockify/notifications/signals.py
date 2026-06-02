from .models import Notification
from django.db.models.signals import post_save
from django.dispatch import receiver
from teams.models import Task

@receiver(post_save, sender=Task)
def create_notification(sender, instance, created, **kwargs):

    if created and instance.assigned_to:
        Notification.objects.create(
            recipient=instance.assigned_to,
            title=instance.title,
            message=f"You have been assigned a new task: '{instance.title}' under team '{instance.team.name}'.",
        )

    elif not created:
        if hasattr(instance, "status") and instance.status in ["DONE", "done"]:
            supervisor = instance.team.supervisor
            Notification.objects.create(
                recipient=supervisor,
                title=f"Task '{instance.title}' is Done",
                message=f"The task '{instance.title}' assigned to {instance.assigned_to.email} has been marked as completed."
            )


