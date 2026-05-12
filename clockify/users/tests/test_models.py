import pytest
from users.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        
        user = UserFactory()

        assert user.email is not None

    def test_string_representation(self):

        user = UserFactory()

        assert str(user) == user.email
