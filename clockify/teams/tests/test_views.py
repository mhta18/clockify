import pytest
from rest_framework.test import APIClient
from users.tests.factories import UserFactory
from teams.tests.factories import TeamFactory
from rest_framework import status
from django.urls import reverse


@pytest.mark.django_db
class TestTeamViewSet:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()

        self.client.force_authenticate(user=self.user)

        self.list_url = reverse("teams-list")

    def test_authentication_request_fails(self):
        
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
