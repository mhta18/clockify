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

        EmployerContractFactory(
            user=self.emp_woman, monthly_payment=Decimal("3520.00"), employment_type=4
        )
        now = timezone.now()

        TimeLogFactory(
            user=self.fl_man,
            project=self.project,
            start_time=now - timedelta(hours=2),
            end_time=now,
        )
        # ($40 * 3 = $120)
        TimeLogFactory(
            user=self.fl_woman,
            project=self.project,
            start_time=now - timedelta(hours=3),
            end_time=now,
        )
        # ($20 * 5 = $100)
        TimeLogFactory(
            user=self.emp_man,
            project=self.project,
            start_time=now - timedelta(hours=5),
            end_time=now,
        )

        TimeLogFactory(
            user=self.emp_woman, project=self.project, start_time=now, end_time=None
        )

    def test_get_reports_all_users_in_db(self):

        print("\n--- ALL USERS IN DB ---")
        for u in get_user_model().objects.all():
            print(f"ID: {u.id} | Email: {u.email} | Gender: {u.gender} | Age: {u.age}")
        print("-----------------------")

        for t in TimeLogFactory._meta.model.objects.all():
            print(
                f"TimeLog - User: {t.user.email}, Project: {t.project.name}, Start: {t.start_time}, End: {t.end_time}"
            )
        
        response = self.client.get("/api/admin-dashbord/user-reports/")
        self.assertEqual(response.status_code, 200)


    def test_get_reports_http_status_success(self):
        response = self.client.get("/api/admin-dashbord/user-reports/")
        self.assertEqual(response.status_code, 200)

    def test_get_reports_platform_totals_and_financials(self):
        response = self.client.get("/api/admin-dashbord/user-reports/")
        data = response.json()

        totals = data["platform_wide_totals"]
        assert totals["total_completed_hours"] == Decimal("10.00")
        assert Decimal(str(totals["total_processed_payouts"])) == Decimal("320.00")

    def test_get_reports_contract_type_metrics(self):
        response = self.client.get("/api/admin-dashbord/user-reports/")
        data = response.json()

        fl_report = data["freelancer_reports"]
        assert fl_report["total_hours_tracked"] == Decimal("5.00")
        assert Decimal(str(fl_report["total_payout_processed"])) == Decimal("220.00")

        emp_report = data["employer_reports"]
        assert emp_report["total_hours_tracked"] == Decimal("5.00")
        assert Decimal(str(emp_report["total_costs_accumulated"])) == Decimal("100.00")

    def test_get_reports_global_demographics(self):
        response = self.client.get("/api/admin-dashbord/user-reports/")
        data = response.json()

        overview = data["global_overview"]
        assert overview["total_registered_accounts"] == 6
        assert overview["all_men"] == 3
        assert overview["all_women"] == 2
        assert overview["unspecified_gender"] == 1
        assert overview["average_age"] is not None

    def test_summary_for_nonadmin_user(self):
        self.client.force_authenticate(user=self.fl_man)
        response = self.client.get("/api/admin-dashbord/user-reports/")
        assert response.status_code == 403

    def test_man_count_in_reports(self):
        response = self.client.get("/api/admin-dashbord/user-reports/")
        data = response.json()

        overview = data["freelancer_reports"]
        assert overview["men_count"] == 1