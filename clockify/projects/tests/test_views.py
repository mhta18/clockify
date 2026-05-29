from projects.models import Project
from teams.models import Team
from teams.tests.factories import TeamFactory
from rest_framework.test import APITestCase
from .factories import ProjectFactory
from django.urls import reverse
from rest_framework.test import APIClient
from users.tests.factories import UserFactory
from rest_framework import status


class ProjetcViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory(is_admin=True)

        self.team_1 = TeamFactory.create(name="DevOps")
        self.team_2 = TeamFactory.create(name="Frontend Devs")

        self.project = ProjectFactory(
            name="Alpha Platform", teams=[self.team_1, self.team_2]
        )

        self.list_create_url = reverse("project-list")
        self.detail_url = reverse("projects-detail", kwargs={"pk": self.project.id})

    def test_list_projects_returns_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "Alpha Platform")

    def test_create_projects_returns_success(self):
        payload = {
            "name": "new project",
            "teams": [self.team_1.id, self.team_2.id],
        }
        self.client.force_authenticate(user=self.user)
        router_create_url = reverse("projects-list")
        response = self.client.post(router_create_url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_projects_returns_success(self):
        payload = {
            "name": "upgraded Alpha",
            "teams": [self.team_1.id, self.team_2.id],
        }
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(self.detail_url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "upgraded Alpha")

    def test_delete_projects_return_success(self):
        payload = {
            "name": "Beta Project",
            "teams": [self.team_1.id, self.team_2.id],
        }

        self.client.force_authenticate(user=self.user)
        router_create_url = reverse("projects-list")
        create_response = self.client.post(
            router_create_url, data=payload, format="json"
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        delete_response = self.client.delete(
            self.detail_url, data=payload, format="json"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

    def test_batch_generation_speed_tip(self):

        ProjectFactory.create_batch(10)

        response = self.client.get(self.list_create_url)
        self.assertEqual(len(response.data), 1)
