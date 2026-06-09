from django.utils import timezone
from datetime import timedelta
from notifications.models import Notification
from users.tests.factories import UserFactory
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        one_month_ago = timezone.now() - timedelta(days=30)

        deleted_count = Notification.objects.filter(created_at__lt=one_month_ago).delete()

        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {deleted_count} old notifications."))
