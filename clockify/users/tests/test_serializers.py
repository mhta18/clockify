import pytest
import json
from users.serializers import UserSerializer


@pytest.mark.django_db
def test_user_serializer():

    data = {
            "email": "test@gmail.com",
            "first_name": "lion",
            "last_name": "lion",
            "phone_number": "+1234567890",
            "gender": "female",          # Or whatever your choices dictate
            "country": "US",
            "age": 25,
            "birth_date": "2001-01-01"
        }
    serializer = UserSerializer(data=data)
    assert serializer.is_valid()
    print("\n" + json.dumps(serializer.errors, indent=4))

