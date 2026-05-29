import pytest
from authentication.serializers import RequestOTPSerializer
from users.tests.factories import UserFactory

@pytest.mark.django_db
class TestRequestOTPSerializer:
    def test_valid_serializer(self):
        user = UserFactory(email="test@gmail.com")
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
