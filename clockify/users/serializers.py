from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    avatar = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "gender",
            "avatar",
            "birth_date",
            "is_active",
            "is_admin",
        )
