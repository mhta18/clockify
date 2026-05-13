from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema

from datetime import timedelta

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .models import LoginOTP
from .serializers import (
    RequestOTPSerializer,
    VerifyOTPSerializer,
)

from .utils import generate_otp
from .services import send_otp_email



# url_path = method name


class AuthViewSet(viewsets.ViewSet):

    @extend_schema(
        request=RequestOTPSerializer,
    )
    @action(detail=False, methods=["post"])
    def request_otp(self, request):

        serializer = RequestOTPSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        code = generate_otp().upper()

        LoginOTP.objects.create(
            email=email,
            code=code,
        )

        send_otp_email(email, code)

        return Response({"message": "OTP sent successfully"})

    @extend_schema(
        request=VerifyOTPSerializer,
    )
    @action(detail=False, methods=["post"])
    def verify_otp(self, request):

        serializer = VerifyOTPSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = serializer.save()

        return Response(data)
