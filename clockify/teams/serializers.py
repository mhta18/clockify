from rest_framework import serializers
from teams.models import Team
from users.serializers import UserSerializer


class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
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
