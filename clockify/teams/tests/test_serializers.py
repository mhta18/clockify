import pytest
from users.serializers import UserSerializer


@pytest.mark.django_db
def test_user_serializer():

    data = {
        "email": "test@gmail.com",
        "first_name": "lion",
        "last_name": "lion",
        "is_active": True,
    }

    serializer = UserSerializer(data=data)

    assert serializer.is_valid()
