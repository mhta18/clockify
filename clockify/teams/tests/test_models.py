# teams/tests/test_models.py
import pytest
from teams.tests.factories import (
    TeamFactory,
)  # 🟢 Fixed typo: TeamFactrory -> TeamFactory


@pytest.mark.django_db
class TestTeamsModel:

    def test_create_team(self):
        # Act
        team = TeamFactory()

        # Assert
        assert team.supervisor is not None
        # Pro-tip: Also assert that your post_generation hook worked!
        assert team.members.filter(id=team.supervisor.id).exists()

    def test_string_representation(self):
        # Act
        team = TeamFactory()

        # Assert
        assert str(team) == team.name
