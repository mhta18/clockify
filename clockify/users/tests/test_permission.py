import pytest 

from users.permissions import IsAdminUser


@pytest.mark.django_db
def test_is_admin_user_permission():

    permission = IsAdminUser()

    user = type("User", (),{"is_authenticated": True, "is_admin": True})()
    request = type("Request", (), {"user": user})()

    assert permission.has_permission(request, None) == True