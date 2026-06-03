import os
from rest_framework import serializers
from teams.models import Team, Task
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
            # POST/PUT request
            "supervisor",
            "members",
            # Get request
            "supervisor_details",
            "members_details",
        ]
        read_only_fields = ["id", "slug", "created_at", "member_count"]

    # for post/put request to write the ID
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

    def to_internal_value(self, data):
        internal_value = data.copy()

        if "members" in internal_value:
            raw_members = internal_value.getlist("members")

            if (
                len(raw_members) == 1
                and isinstance(raw_members[0], str)
                and "," in raw_members[0]
            ):
                raw_members = raw_members[0].split(",")

            try:

                cleaned_members = [
                    int(m) for m in raw_members if str(m).strip().isdigit()
                ]
                internal_value.setlist("members", cleaned_members)
            except (ValueError, TypeError):
                pass

        return super().to_internal_value(internal_value)

    def validate_Logo_size(self, attrs):

        valid_extension = ["jpg", "jpeg", "png"]
        ext = os.path.splitext(attrs.name)[1][1:].lower()

        if ext not in valid_extension:
            raise serializers.ValidationError(
                f"Unsupported file extension. Allowed extensions are: {', '.join(valid_extension)}"
            )
        max_size = 5 * 1024 * 1024  # 5MB

        if attrs.size > max_size:
            raise serializers.ValidationError(
                "File size exceeds the maximum limit of 5MB."
            )

        return attrs

    def validate_Logo_team_name(self, attrs):
        team_name = attrs.get("name")
        team_logo = attrs.get("logo")

        if team_name and team_logo:
            requeired_name = team_name.strip().lower()

            file_name_without_extension = os.pah.splitext(team_logo.name)[0].lower()

            if requeired_name not in file_name_without_extension:
                raise serializers.ValidationErrorserializers.ValidationError(
                    {
                        "logo": f"The uploaded file name must contain the team's name. "
                        f"Expected to find '{requeired_name}' inside '{file_name_without_extension}'."
                    }
                )

        return attrs


class TaskSerializer(serializers.ModelSerializer):

    created_by = serializers.ReadOnlyField(source="created_by.email")
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status_display",
            "team",
            "created_by",
            "assigned_to",
            "deadline",
            "priority",
        ]

    def validate(self, attrs):

        request_user = self.context["request"].user
        team = attrs.get("team")
        if team and team.supervisor != request_user:
            raise serializers.ValidationError(
                {
                    "team": f"You cannot manage tasks for '{team.name}' because you are not its assigned supervisor."
                }
            )

        return super().validate(attrs)


class TaskMemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "deadline",
            "status",
            "priority",
            "team",
            "assigned_to",
        ]

        read_only_fields = [
            "id",
            "title",
            "description",
            "deadline",
            "priority",
            "team",
            "assigned_to",
        ]

    def validate(self, attrs):

        team = attrs.get("team")
        assigned_to = attrs.get("assigned_to")
        if team and assigned_to and assigned_to not in team.members.all():
            raise serializers.ValidationError(
                {
                    "assigned_to": f"The user '{assigned_to.email}' is not a member of '{team.name}'."
                }
            )

        return super().validate(attrs)
