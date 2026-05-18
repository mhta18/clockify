from rest_framework import serializers
from teams.models import Team
from users.serializers import UserSerializer


class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    member_count = serializers.IntegerField()
    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "created_at",
            "members",
        ]
        read_only_fields = ["id", "slug", "created_at","member_count"]
