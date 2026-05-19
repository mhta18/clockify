# teams/tests/test_models.py
import pytest
from teams.tests.factories import (
    TeamFactory,
)  


@pytest.mark.django_db
class TestTeamsModel:

    def test_create_team(self):
    
        team = TeamFactory()
        assert team.supervisor is not None

        assert team.members.filter(id=team.supervisor.id).exists()

    def test_string_representation(self):

        team = TeamFactory()
        assert str(team) == team.name
