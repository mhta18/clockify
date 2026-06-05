from celery import shared_task
from django.core.management import call_command

@shared_task
def auto_clear_old_notifications():
    call_command("clear_old_notifications")