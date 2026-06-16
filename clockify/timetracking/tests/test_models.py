import pytest
from django.utils import timezone
from datetime import timedelta
from .factories import TimeLogFactory
from contracts.tests.factories import FreelancerContractFactory
from decimal import Decimal
from users.tests.factories import UserFactory

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

        assert log.duration.total_seconds() == 0

    def test_payment_calculated_from_contract_on_stop(self):

        user = UserFactory()
        FreelancerContractFactory(user=user, hourly_payment=Decimal("50.00"))

        start = timezone.now() - timedelta(hours=2)
        end = timezone.now()

        log = TimeLogFactory(user=user, start_time=start, end_time=end)
        assert log.payment == Decimal("100.00")
