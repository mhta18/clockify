import pytest


from authentication.serializers import RequestOTPSerializer


class TestRequestOTPSerializer:
    def test_valid_serializer(self):

        serializer = RequestOTPSerializer(
            data = {
                "email":"test@gmail.com"
            }
        )

        assert serializer.is_valid()

    def test_invalid_email(self):

        serializer = RequestOTPSerializer(
            data={
                "email":"invalid_email"
            }
        )

        assert not serializer.is_valid()