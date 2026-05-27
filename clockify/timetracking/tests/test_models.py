import pytest
from django.utils import timezone
from datetime import timedelta
from .factories import TimeLogFactory
from rest_framework.test import APIClient
from users.tests.factories import UserFactory
from teams.tests.factories import TeamFactory
from projects.tests.factories import ProjectFactory
from contracts.tests.factories import EmployerContract

pytestmark = pytest.mark.django_db


class TestTimeTracking:

    def test_duration_for_completed_task(self):
        start = timezone.now() - timedelta(hours=2)
        end = timezone.now()

        log = TimeLogFactory(start_time=start, end_time=end)
        assert log.duration == timedelta(hours=2)

    def test_duration_property_for_running_timer(self):
        start = timezone.now() - timedelta(minutes=45)
        log = TimeLogFactory(start_time=start, end_time=None)

        assert abs(log.duration.total_seconds() - 2700) < 2


