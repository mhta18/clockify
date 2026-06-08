from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from .models import LoginOTP
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RequestOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):

        if not User.objects.filter(email=value).exists():

            raise serializers.ValidationError("Invalid credentials")

        return value


class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    code = serializers.CharField()

    def validate(self, attrs):

        email = attrs["email"]

        code = attrs["code"].upper()

        otp = LoginOTP.objects.filter(
            email=email,
            code=code,
            is_used=False,
        ).last()

        if not otp:

            raise serializers.ValidationError("Invalid code")

        if (
            otp.created_at + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
            < timezone.now()
        ):

            raise serializers.ValidationError("Code expired")

        attrs["otp"] = otp

        return attrs

    def create(self, validated_data):

        email = validated_data["email"]

        otp = validated_data["otp"]

        otp.is_used = True

        otp.save()

        user = User.objects.get(email=email)

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "is_admin": user.is_admin,
            },
        }
