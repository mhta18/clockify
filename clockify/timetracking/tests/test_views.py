import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from users.tests.factories import UserFactory
from projects.tests.factories import ProjectFactory
from django.urls import reverse
from rest_framework import status
from timetracking.tests.factories import TimeLogFactory
from teams.tests.factories import TeamFactory
from contracts.tests.factories import FreelancerContractFactory
from timetracking.models import TimeLog
pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    client = APIClient()
    admin_user = UserFactory(is_admin =True)
    client.force_authenticate(user=admin_user)
    return client, admin_user

class TestTimeLogViewSet:

    def test_create_timelog_success(self,api_client):
        client, user= api_client
        FreelancerContractFactory(user=user)
        team = TeamFactory(members=[user.id])
        project = ProjectFactory(teams=[team.id])
        url = reverse("timelog-list")

        data = {
            
            "project": project.id, 
            "description": "new task",
        }

        response= client.post(url,data=data,format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["description"] == "new task"

    def test_resume_action_creates_cloned_log_entry(self, api_client):
        client, user = api_client
        FreelancerContractFactory(user=user)
        team = TeamFactory(members=[user.id])
        project = ProjectFactory(teams=[team.id])
        past_log = TimeLogFactory(
            user=user,
            project=project,
            description="Legacy code branch",
            end_time=timezone.now(),
        )

        url = reverse(
            "timelog-resume", kwargs={"pk": past_log.id}
        ) 
        response = client.post(url)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["description"] == "Legacy code branch"
        assert response.data["id"] != past_log.id  # Must be a brand new instance ID
        assert response.data["is_running"] is True

    def test_delete_timlog_record(self,api_client):
        client, user = api_client
        FreelancerContractFactory(user=user)
        log = TimeLogFactory(user=user)
        url = reverse("timelog-detail", kwargs={"pk": log.id})

        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not TimeLog.objects.filter(id=log.id).exists()