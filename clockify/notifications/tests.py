from django.test import TestCase
from notifications.models import Notification
from teams.tests.factories import TeamFactory
from users.tests.factories import UserFactory
from teams.tests.factories import TaskFactory

# Create your tests here.


class NotificationsTestCase(TestCase):

    def test_notification_sent_to_member_on_task_creation(self):

        supervisor = UserFactory(email="supervisor@test com", gender="other", age=34)
        member = UserFactory(email="member@test com", gender="male", age=30)
        team = TeamFactory(supervisor=supervisor, members=[member.id])

        TaskFactory(
            title="Test Task 1",
            team=team,
            assigned_to=member,
            created_by=supervisor,
        )

        notification = Notification.objects.filter(recipient=member).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.title, "Test Task 1")
        self.assertEqual(notification.recipient, member)

    def test_notification_sent_to_supervisor_on_task_completion(self):
        supervisor = UserFactory(email="supervisor@test.com", gender="other", age=34)
        member = UserFactory(email="worker@test.com", gender="male", age=30)
        team = TeamFactory(supervisor=supervisor,members=[member])

        task = TaskFactory(
            title="Refactor DB", team=team, assigned_to=member, created_by=supervisor, status="IN_PROGRESS"
        )

        Notification.objects.all().delete()

        task.status = "DONE"
        task.save()

        notification = Notification.objects.filter(recipient=supervisor).first()
        assert notification is not None
        assert f"Task '{task.title}' is Done" in notification.title
        assert "worker@test.com" in notification.message
