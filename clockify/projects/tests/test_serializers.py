import pytest
from django.test import TestCase
from users.tests.factories import UserFactory
from teams.tests.factories import TeamFactory
from django.utils.datastructures import MultiValueDict
from projects.serializers import ProjectSerializer
from projects.models import Project

class ProjectSerializerTest(TestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.team_1 = TeamFactory.create()
        self.team_2 = TeamFactory.create()

        self.base_data = MultiValueDict({
            "name": ["commerce system"],
            "teams": [str(self.team_1.id), str(self.team_2.id)]
        })

    def test_valid_project_serializetion(self):

        serializer = ProjectSerializer(data=self.base_data)
        self.assertTrue(serializer.is_valid(),serializer.errors)

        project = serializer.save()
        self.assertEqual(project.name,"commerce system")
        self.assertEqual(project.teams.count(),2)

    def test_valid_project_with_optional_end_date(self):
        self.base_data.setlist("end_date", ["2026-12-21"])
        serializer = ProjectSerializer(data=self.base_data)
        self.assertTrue(serializer.is_valid())
