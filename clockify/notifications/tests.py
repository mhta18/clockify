from django.test import TestCase
import pytest
from unittest.mock import patch
from teams.models import Task
from rest_framework.test import APIClient
from projects.tests.factories import ProjectFactory
from teams.tests.factories import TeamFactory
from users.tests.factories import UserFactory
from teams.tests.factories import TaskFactory
from django.core.management import call_command
from django.utils import timezone
from .models import Notification

# Create your tests here.
pytestmark = pytest.mark.django_db


class NotificationsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = UserFactory(
            is_admin=True, email="admin@test.com", gender="male", age=30
        )
        self.client.force_authenticate(user=self.admin_user)

    @patch("teams.views.broadcast_notification")
    def test_notification_sent_to_member_on_task_creation(self, mock_send_notification):

        supervisor = UserFactory(email="supervisor@test com", gender="other", age=34)
        member = UserFactory(email="member@test com", gender="male", age=30)
        team = TeamFactory(supervisor=supervisor, members=[member.id],name= "Backend first")
        self.client.force_authenticate(user=supervisor)
        payload = {
            "title": "Build WebSocket Interface",
            "created_by": supervisor.id,
            "team": "Backend first",
            "assigned_to": member.id,
            "deadline": "2026-05-30T17:00:00Z",
            "status": "TODO",
        }

        response = self.client.post("/api/supervisor/tasks/", data=payload)
        print("/////////////////////////////////",response.data)
        assert response.status_code == 201
        mock_send_notification.assert_called_once()
        called_recipient = mock_send_notification.call_args[1]["recipient"]
        assert called_recipient == member

    @patch("teams.views.broadcast_notification")
    def test_notification_sent_to_supervisor_on_task_completion(
        self, mock_send_notification
    ):
        supervisor = UserFactory(email="supervisor@test.com", gender="other", age=34)
        member = UserFactory(email="worker@test.com", gender="male", age=30)
        team = TeamFactory(supervisor=supervisor, members=[member])
        self.client.force_authenticate(user=member)
        task = TaskFactory(
            team=team,
            created_by=supervisor,
            assigned_to=member,
            status=Task.Status.IN_PROGRESS,
            priority=Task.Priority.HIGH,
        )
        payload = {"status": Task.Status.DONE}

        response = self.client.patch(f"/api/my-tasks/update/{task.id}/", data=payload)
        print("////////////////////////////////////////////////////////", response.data)
        assert response.status_code == 200
        updated_task = Task.objects.get(id=task.id)
        mock_send_notification.assert_called_once()
        kwargs = mock_send_notification.call_args[1]
        assert kwargs["recipient"] == supervisor
        assert kwargs["title"] == task.title
        assert updated_task.status == Task.Status.DONE


class NotificationCleanupTest(TestCase):

    def test_clear_old_notification(self):

        user = UserFactory(email="mahta@gmail.com")
        now = timezone.now()

        Notification.objects.create(
            recipient=user, title="new", message="existing message", created_at=now
        )

        old_notification = Notification.objects.create(
            recipient=user, title="old", message="old message"
        )

        Notification.objects.filter(
            id=old_notification.id).update(created_at=now - timezone.timedelta(days=32))

        call_command("clear_old_notifications")

        remaining_notifications = Notification.objects.filter(recipient=user)

        self.assertEqual(remaining_notifications.count(), 1)
