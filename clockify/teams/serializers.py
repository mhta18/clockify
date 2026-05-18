from rest_framework import serializers
from teams.models import Team
from users.serializers import UserSerializer


class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)
    supervisor = UserSerializer(source="supervisor",read_only=True)
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
            "members",
        ]
        read_only_fields = ["id", "slug", "created_at","member_count"]

    def validate(self, data):
        supervisor = data.get("supervisor")
        members = data.get("members", [])

        # If we are updating an existing instance, grab current members if not provided in payload
        if self.instance and "members" not in data:
            members = list(self.instance.members.all())

        if supervisor and supervisor not in members:
            raise serializers.ValidationError(
                {
                    "supervisor": "The supervisor must be assigned as a member of the team."
                }
            )
        return data
