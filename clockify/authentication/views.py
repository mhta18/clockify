from datetime import timedelta

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response    
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from .models import LoginOTP
from .serializaers import RequestOTPSerializer,VerifyOTPSerializer
from .services import send_otp_email
from .utils import generate_otp
from django.conf import settings
from django.utils import timezone

# Create your views here.

class RequestOTPView(APIView):
    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = generate_otp()
            LoginOTP.objects.create(email=email, code=code)
            send_otp_email(email, code)
            return Response({"message": "OTP sent to your email!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):

            serializer = VerifyOTPSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            email = serializer.validated_data["email"]
            code = serializer.validated_data["code"]

            otp = LoginOTP.objects.filter(email=email,code=code,is_used=False).last()

            if not otp:
                return Response(
                    {"error": "Invalid code"},
                    status=400
                )
            

            if otp.created_at + timedelta(minutes=settings.OTP_EXPIRE_MINUTES) < timezone.now():
                return Response(
                    {"error": "Code expired!"},
                    status=400
                )
            otp.is_used = True
            otp.save()

            # find user
            from django.contrib.auth import get_user_model

            User = get_user_model()

            try:
                user = User.objects.get(email=email)

            except User.DoesNotExist:
                return Response(
                    {"error": "User does not exist"},
                    status=404
                )

            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            })