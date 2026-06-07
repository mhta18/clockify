import pytest

from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
from users.tests.factories import UserFactory

@pytest.mark.django_db
class TestRequestOPTView:

    def setup_method(self):
        self.client = APIClient()

    def test_request_otp_success(self):
        user = UserFactory(
            email="lion@gmail.com",
        )
        response = self.client.post(
            "/api/auth/request_otp/", {"email": user.email}, format="json"
        )
        assert response.status_code == 200

    def test_request_otp_invalid_user(self):
        response = self.client.post(
            "/api/auth/request_otp/", {"email": "m@gmail.com"}, format="json"
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestAuthRateLimiting:

    def test_request_otp_rate_limiting_block_request_after_5_attemps(self):
        cache.clear()
        client = APIClient()
        user = UserFactory(
            email="user@example.com",
        )
        url = "/api/auth/request_otp/"
        payload = {"email": user.email}

        for i in range(5):
            response = client.post(url,data=payload,format="json")
            print("//////////////////////////////////////////////", response.data)
            assert (
                response.status_code == status.HTTP_200_OK
            ), f"Request {i+1} failed unexpectedly."

        throttle_request = client.post(url,data=payload, format="json")

        assert throttle_request.status_code == status.HTTP_429_TOO_MANY_REQUESTS
