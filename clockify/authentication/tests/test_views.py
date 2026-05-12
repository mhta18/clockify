import pytest

from rest_framework.test import APIClient

from users.tests.factories import UserFactory

@pytest.mark.django_db
class TestRequestOPTView:
   
    def setup_method(self):
        self.client = APIClient()

    def test_request_otp_success(self):
        user = UserFactory(
            email="m@gmail.com",
        )
        response = self.client.post(
            "/api/auth/request_otp/", {"email": user.email}, format="json"
        )
        assert response.status_code == 200

    def test_request_otp_invalid_user(self):
        response = self.client.post(
            "/api/auth/request_otp/", {"email": "noone@gmail.com"}, format="json"
        )
        assert response.status_code == 404
