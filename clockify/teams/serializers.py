from rest_framework import serializers
from teams.models import Team
from users.serializers import UserSerializer


class TeamSerializer(serializers.ModelSerializer):
    supervisor_details = UserSerializer(source="supervisor", read_only=True)
    members_details = UserSerializer(source="members", many=True, read_only=True)
    member_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "slug",
            "logo",
            "description",
            "created_at",
            "member_count",
            # PUT request
            "supervisor",
            "members",
            # Get request
            "supervisor_details",
            "members_details",
        ]
        read_only_fields = ["id", "slug", "created_at", "member_count"]
    #for post/put request to write the ID
    def validate(self, data):
        supervisor = data.get("supervisor")
        members = data.get("members", [])

        if self.instance and "members" not in data:
            members = list(self.instance.members.all())

        if supervisor and supervisor not in members:
            raise serializers.ValidationError(
                {
                    "supervisor": "The supervisor must be assigned as a member of the team."
                }
            )
        return data
