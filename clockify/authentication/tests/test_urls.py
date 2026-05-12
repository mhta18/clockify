from django.urls import resolve, reverse

from authentication.views import AuthViewSet


def test_request_otp_url():
    url = reverse("auth-request-otp")
    assert resolve(url).func.cls == AuthViewSet
