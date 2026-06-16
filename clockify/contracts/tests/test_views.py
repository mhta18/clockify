import pytest
from rest_framework.test import APIClient
from users.tests.factories import UserFactory
from datetime import date, timedelta
from rest_framework import status
from django.urls import reverse
from contracts.models import FreelancerContract, EmployerContract
from contracts.tests.factories import FreelancerContractFactory, EmployerContractFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    client = APIClient()
    admin_user = UserFactory(is_admin=True)
    client.force_authenticate(user=admin_user)
    return client


class TestEmployerContractView:

    def test_list_freelancer_contracts_via_list_view(self, api_client):
        FreelancerContractFactory.create_batch(3)

        url = reverse("freelancer-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create_freelancer_contract_vie_viewset(self, api_client):
        user = UserFactory()

        url = reverse("freelancers-list")

        data = {
            "user": user.id,
            "role_title": "Frontend Developer",
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=90)),
            "hourly_payment": "45",
            "daily_hours_required": 8,
        }

        response = api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_freelancer_contract_via_viewset(self, api_client):
        freelancer_contract = FreelancerContractFactory(role_title="React Developer")

        url = reverse("freelancers-detail", kwargs={"pk": freelancer_contract.id})

        data = {
            "user": freelancer_contract.user.id,
            "role_title": "Team Lead",
            "start_date": str(freelancer_contract.start_date),
            "end_date": str(freelancer_contract.end_date),
            "hourly_payment": "40.00",
            "daily_hours_required": 8,
        }

        response = api_client.put(url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_delete_freelancer_contract_via_viewset(self, api_client):
        freelancer_contract = FreelancerContractFactory(role_title="React Developer")

        url = reverse("freelancers-detail", kwargs={"pk": freelancer_contract.id})

        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not FreelancerContract.objects.filter(id=freelancer_contract.id).exists()


class TestEmployerContractView:

    def test_list_Employer_contracts_via_list_view(self, api_client):
        EmployerContractFactory.create_batch(3)

        url = reverse("employer-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create_Employer_contract_vie_viewset(self, api_client):
        user = UserFactory()

        url = reverse("employers-list")

        data = {
            "user": user.id,
            "role_title": "React Developer",
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=90)),
            "monthly_payment": "450",
            "employment_type": EmployerContract.EmploymentHours.FOUR_HOURS,
        }

        response = api_client.post(url, data=data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_Employer_contract_via_viewset(self, api_client):
        employer_contract = EmployerContractFactory(role_title="React Developer")

        url = reverse("employers-detail", kwargs={"pk": employer_contract.id})

        data = {
            "user": employer_contract.user.id,
            "role_title": "React Developer",
            "start_date": str(date.today()),
            "end_date": str(date.today() + timedelta(days=90)),
            "monthly_payment": "450",
            "employment_type": EmployerContract.EmploymentHours.FIVE_HOURS,
        }
        response = api_client.put(url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_delete_Employer_contract_via_viewset(self, api_client):
        employer_contract = EmployerContractFactory(role_title="React Developer")

        url = reverse("employers-detail", kwargs={"pk": employer_contract.id})

        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not EmployerContract.objects.filter(id=employer_contract.id).exists()
