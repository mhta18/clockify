import pytest
from rest_framework.test import APIClient
from users.tests.factories import UserFactory
from teams.tests.factories import TeamFactory
from rest_framework import status
from django.urls import reverse
from freezegun import freeze_time
from django.core.files.uploadedfile import SimpleUploadedFile


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

    def test_list_team_include_member_count(self):

        team = TeamFactory()

        response = self.client.get(self.list_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1 

        assert response.data[0]["member_count"] == 1
        assert response.data[0]["name"] == team.name

    def test_create_team_with_logo_upload(self):
        supervisor_user = UserFactory()

        fake_logo = SimpleUploadedFile(
            name="test_logo.gif",
            content=b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b",
            content_type="image/gif"
        )

        payload = {
            "name": "Cloud Operations",
            "description": "Managing AWS infrastructure",
            "supervisor": supervisor_user.id,
            "members": [supervisor_user.id],
            "logo": fake_logo, 
        }

        response = self.client.post(self.list_url,data=payload,format="multipart")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Cloud Operations"
        assert "logo" in response.data
        assert response.data["logo"] is not None

    def test_create_invalid_supervisor_fails(self):
        supervisor_user = UserFactory()
        another_user = UserFactory()

        payload = {
            "name": "team 1",
            "supervisor": supervisor_user.id,
            "members":[another_user.id]
        }

        response = self.client.post(self.list_url,data=payload,format="multipart")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "supervisor" in response.data

    def test_search_by_name(self):
        TeamFactory(name="DevOps Team")
        TeamFactory(name="Backend Team")

        response = self.client.get(self.list_url,data={"search" : "Backend"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Backend Team"

    def test_search_by_description(self):
        TeamFactory(description="DevOps Team 1")
        TeamFactory(description="Backend Team 2")

        response = self.client.get(self.list_url, data={"search": "DevOps"})

        assert response.data[0]["description"] =="DevOps Team 1"

    def test_ordering_teams_by_name(self):
        TeamFactory(name="Alpha Team")
        TeamFactory(name="Backend Team")

        response = self.client.get(self.list_url,data={"ordering" : "name"})

        assert response.data[0]["name"] == "Alpha Team"

    def test_filter_by_createdAt(self):

        with freeze_time("2026-05-16 12:00:00"):
            TeamFactory(name="Team 1")
        with freeze_time("2026-05-17 12:00:00"):
            TeamFactory(name="Team 2")
        response = self.client.get(self.list_url, {"created_at": "2026-05-16 12:00:00"})

        assert response.status_code == 200
        assert len(response.data) == 1

    def test_ordering_by_createdAt(self):

        with freeze_time("2026-05-16 12:00:00"):
            TeamFactory(name="Team 1")
        with freeze_time("2026-05-17 12:00:00"):
            TeamFactory(name="Team 2")
        response = self.client.get(self.list_url,{"ordering": "created_at"})

        assert response.status_code == 200
        assert response.data[0]["name"]== "Team 1"