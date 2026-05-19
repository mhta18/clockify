import pytest
from teams.tests.factories import TeamFactory
from users.tests.factories import UserFactory
from teams.serializers import TeamSerializer
class TestTeamSerializer:

    #write data
    @pytest.mark.django_db
    def test_serialize_valid_team(self):
        team = TeamFactory()
        serializer = TeamSerializer(instance=team)
        
        assert serializer.data['name'] == team.name
        assert serializer.data['supervisor_details']['id'] == team.supervisor.id

    #read data
    @pytest.mark.django_db
    def test_deserialize_valide_date(self):
        user = UserFactory()
        user1 = UserFactory()
        team = TeamFactory(supervisor=user)

        payload = {
            "name": "devops",
            "description": "description 1",
            "supervisor": user.id, 
            "members": [user.id,user1.id],
        }

        serializer = TeamSerializer(data=payload)
        assert serializer.is_valid() is True
