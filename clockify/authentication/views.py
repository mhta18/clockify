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

User = get_user_model()

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

        try:
            User.objects.get(email=email)

        except User.DoesNotExist:

            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_404_NOT_FOUND
            )

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

        email = serializer.validated_data["email"]

        code = serializer.validated_data["code"].upper()

        otp = LoginOTP.objects.filter(
            email=email,
            code=code,
            is_used=False,
        ).last()

        if not otp:

            return Response(
                {"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST
            )

        if (
            otp.created_at + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
            < timezone.now()
        ):

            return Response(
                {"error": "Code expired"}, status=status.HTTP_400_BAD_REQUEST
            )

        otp.is_used = True
        otp.save()

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:

            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "is_admin": user.is_admin,
                },
            }
        )
