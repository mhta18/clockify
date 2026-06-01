import pytest
from django.test import TestCase
from teams.tests.factories import TeamFactory
from contracts.tests.factories import EmployerContractFactory, FreelancerContractFactory
from users.tests.factories import UserFactory
from rest_framework.test import APIClient
from projects.tests.factories import ProjectFactory
from timetracking.tests.factories import TimeLogFactory
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal

# Create your tests here.

pytestmark = pytest.mark.django_db


class ReportsViewSetTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = UserFactory(
            is_admin=True, email="admin@test.com", gender="male", age=30
        )
        self.client.force_authenticate(user=self.admin_user)

        self.project = ProjectFactory(name="Test Project")

        self.fl_man = UserFactory(
            gender="male", email="freelancer.man@test.com", age=25
        )
        self.fl_woman = UserFactory(
            gender="female", email="freelancer.woman@test.com", age=28
        )

        FreelancerContractFactory(user=self.fl_man, hourly_payment=Decimal("50.00"))
        FreelancerContractFactory(user=self.fl_woman, hourly_payment=Decimal("40.00"))

        self.emp_man = UserFactory(gender="male", email="employer.man@test.com", age=35)
        self.emp_woman = UserFactory(
            gender="female", email="employer.woman@test.com", age=32
        )

        self.team = TeamFactory(
            name="Test employer Team",
            members=[
                self.emp_man.id,
                self.emp_woman.id,
                self.fl_man.id,
                self.fl_woman.id,
            ],
        )

        self.project.teams.add(self.team)

        EmployerContractFactory(
            user=self.emp_man, monthly_payment=Decimal("3520.00"), employment_type=8
        )

        now = timezone.now()

        TimeLogFactory(
            user=self.fl_man,
            project=self.project,
            start_time=now - timedelta(hours=2),
            end_time=now,
        )
        # Freelancer Woman works 3 hours ($40 * 3 = $120)
        TimeLogFactory(
            user=self.fl_woman,
            project=self.project,
            start_time=now - timedelta(hours=3),
            end_time=now,
        )
        # Employer Man works 5 hours ($20 * 5 = $100)
        TimeLogFactory(
            user=self.emp_man,
            project=self.project,
            start_time=now - timedelta(hours=5),
            end_time=now,
        )

        # 5. Generate a running active log (Should be ignored by the query)
        TimeLogFactory(
            user=self.fl_man, project=self.project, start_time=now, end_time=None
        )

    def test_get_reports(self):

        print("\n--- ALL USERS IN DB ---")
        for u in get_user_model().objects.all():
            print(f"ID: {u.id} | Email: {u.email} | Gender: {u.gender} | Age: {u.age}")
        print("-----------------------")
        response = self.client.get("/api/admin-dashbord/user-reports/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        assert data["platform_wide_totals"]["total_completed_hours"] == Decimal("10.00")
        assert Decimal(
            data["platform_wide_totals"]["total_processed_payouts"]
        ) == Decimal("320.00")
        fl_report = data["freelancer_reports"]
        assert fl_report["total_hours_tracked"] == Decimal("5.00")
        assert Decimal(fl_report["total_payout_processed"]) == Decimal("220.00")
        emp_report = data["employer_reports"]
        assert emp_report["total_hours_tracked"] == Decimal("5.00")
        assert Decimal(emp_report["total_costs_accumulated"]) == Decimal("100.00")
        assert data["global_overview"]["total_registered_accounts"] == 6
        assert data["global_overview"]["all_men"] == 3
        assert data["global_overview"]["all_women"] == 2
        assert data["global_overview"]["unspecified_gender"] == 1
        assert data["global_overview"]["average_age"] is not None

    def test_summary_for_nonadmin_user(self):
        self.client.force_authenticate(user=self.fl_man)
        response = self.client.get("/api/admin-dashbord/user-reports/")
        assert response.status_code == 403
