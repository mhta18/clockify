import io
import pytest
from teams.serializers import TeamSerializer
from django.test import TestCase
from django.contrib.auth import get_user_model
from users.tests.factories import UserFactory
from teams.tests.factories import TeamFactory
from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import SimpleUploadedFile
User = get_user_model()


class TeamTestSerializer(TestCase):

    @pytest.mark.django_db
    def test_team_serializer(self):
        supervisor = UserFactory.create()
        member1= UserFactory.create()
        member2 = UserFactory.create()

        mock_team = TeamFactory.build(name="Alpha Team")
        valid_logo = mock_team.logo

        input_data = MultiValueDict({
                "name" : ["ALpha"],
                "description" :["description"],
                "logo" : [valid_logo],
                "supervisor":[supervisor.id],
                "members":[member1.id,member2.id,supervisor.id]
            })
        serializer = TeamSerializer(data=input_data)
        self.assertTrue(serializer.is_valid(),serializer.errors)

        team= serializer.save()
        self.assertEqual(team.name,"ALpha")
        self.assertEqual(team.members.count(),3)

    def test_team_invalid_logo_serializer(self):
        supervisor = UserFactory.create()
        member1 = UserFactory.create()
        member2 = UserFactory.create()

        invalid_logo = "random_file_name.png"

        input_data = MultiValueDict(
            {
                "name": ["Alpha"],
                "description": ["description"],
                "logo": [invalid_logo],
                "supervisor": [supervisor.id],
                "members": [member1.id, member2.id, supervisor.id],
            }
        )
        serializer = TeamSerializer(data=input_data)
        self.assertFalse(serializer.is_valid(),serializer.errors)
        self.assertIn("logo", serializer.errors)

    def test_invalid_size_logo(self):
        supervisor = UserFactory.create()

        oversized_bytes_count = int(2.1*1024*1024)
        huge_file_data = io.BytesIO(b"\x00" * oversized_bytes_count)

        actual_large_file = SimpleUploadedFile(
            name="alpha_team_huge_logo.png",
            content=huge_file_data.getvalue(),
            content_type="image/png",
        )

        input_data = MultiValueDict(
            {
                "name": ["Alpha"],
                "description": ["description"],
                "logo": [actual_large_file],
                "supervisor": [supervisor.id],
                "members": [supervisor.id],
            }
        )
        serializer = TeamSerializer(data=input_data)
        self.assertFalse(serializer.is_valid())

    def test_to_internal_value_handdler(self):
        member1 =UserFactory.create()
        member2 = UserFactory.create()
        member3 = UserFactory.create()

        seperated_input_data = MultiValueDict({
            "name":"Alpha",
            "members":[str(member1.id),str(member2.id),str(member3.id)]
        })

        serializer = TeamSerializer(data = seperated_input_data)
        serializer.is_valid()

        self.assertEqual(serializer.validated_data["members"],[member1,member2,member3])

        comma_input_data = MultiValueDict({
            "name" :["beta team"],
            "members":[f"{member1.id},{member2.id},{member3.id}"]
        })

        serializer_2 = TeamSerializer(data =comma_input_data)
        serializer_2.is_valid()
        self.assertEqual(serializer_2.validated_data["members"],[member1,member2,member3])

    # write data
    def test_serialize_valid_team(self):
        team = TeamFactory()
        serializer = TeamSerializer(instance=team)

        assert serializer.data['name'] == team.name
        assert serializer.data['supervisor_details']['id'] == team.supervisor.id

    #read data
    def test_deserialize_valide_date(self):
        user = UserFactory()
        user1 = UserFactory()
        TeamFactory(supervisor=user)

        payload = MultiValueDict({
            "name": ["devops"],
            "description": ["description 1"],
            "supervisor": [user.id],
            "members": [user.id,user1.id],
        })

        serializer = TeamSerializer(data=payload)
        assert serializer.is_valid() is True
