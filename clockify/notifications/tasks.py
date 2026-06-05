from celery import shared_task
from django.core.management import call_command

@shared_task
def clear_old_notifications():
    call_command("clear_old_notifications")