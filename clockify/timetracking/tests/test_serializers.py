import pytest
from django.utils import timezone
from rest_framework import serializers
from timetracking.serializers import TimeLogSerializer
from timetracking.tests.factories import TimeLogFactory
from users.tests.factories import UserFactory
from projects.tests.factories import ProjectFactory
from teams.tests.factories import TeamFactory
from contracts.tests.factories import EmployerContractFactory

pytestmark = pytest.mark.django_db


class TestTimeLogSerializer:

    def test_serializer_outputs_calculated_fields_correctly(self, rf):
        log = TimeLogFactory()
        request = rf.get("/")
        request.user = log.user
        serializer = TimeLogSerializer(instance=log, context={"request": request})

        assert "duration_seconds" in serializer.data
     
    def test_validation_blocks_creation_if_timer_already_running(self, rf):
        user = UserFactory()
        EmployerContractFactory(user=user)
        team = TeamFactory(members = [user.id])
        project =ProjectFactory(teams=[team.id])
        TimeLogFactory(user=user, project=project, end_time=None)
        request = rf.post("/")
        request.user = user

        payload = {"project": project.id, "description": "Trying to cheat the system"}
        serializer = TimeLogSerializer(data=payload, context={"request": request})

        with pytest.raises(serializers.ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

