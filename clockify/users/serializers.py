from rest_framework import request, serializers
import os

from .models import User


class UserSerializer(serializers.ModelSerializer):

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
            "country",
            'age',
            "birth_date",
            "is_active",
            "is_admin",
            "created_at",
            "updated_at",
        )

        read_only_fields = ("created_at", "updated_at")

    def validate_avatar_size(self, attrs):

        # Validate file extension and size
        valid_extension = ['jpg', 'jpeg', 'png']
        ext = os.path.splitext(attrs.name)[1][1:].lower()

        if ext not in valid_extension:
            raise serializers.ValidationError(
                f"Unsupported file extension. Allowed extensions are: {', '.join(valid_extension)}"
            )
        max_size = 5*1024*1024  # 5MB

        if attrs.size > max_size:
            raise serializers.ValidationError("File size exceeds the maximum limit of 5MB.")

        return attrs

    def validate_avatar_name(self, attrs):

        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError("User must be authenticated to upload an avatar.")
        user = request.user

        requeired_name = (user.first_name or user.last_name)

        file_name_without_extension = os.path.splitext(attrs.name)[0].lower()
        if not requeired_name in file_name_without_extension:
            raise serializers.ValidationError(
                f"File name must contain the user's first name, last name, or email prefix. Expected to find '{requeired_name}' in the file name."
            )
        return attrs
