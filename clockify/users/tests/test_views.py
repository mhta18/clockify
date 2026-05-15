import pytest

from rest_framework.test import APIClient

from users.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserViewSet:

    def setup_method(self):
        self.client = APIClient()

    def test_admin_can_list_users(self):

        admin_user = UserFactory(is_admin=True)

        UserFactory.create_batch(3)

        self.client.force_authenticate(user=admin_user)

        response = self.client.get("/api/list/")

        assert response.status_code == 200

        assert len(response.data) >= 3

    def test_non_admin_cannot_list_users(self):

        self.client = APIClient()

        user = UserFactory(is_admin=False)

        self.client.force_authenticate(user=user)

        response = self.client.get("/api/list/")

        assert response.status_code == 403

    def test_admin_can_create_user(self):

        self.client = APIClient()

        admin = UserFactory(is_admin=True)

        self.client.force_authenticate(user=admin)

        response = self.client.post(
            "/api/users/",
            data={
                "email": "test@gmail.com",
                "first_name": "lion",
                "last_name": "lion",
                "gender": "male",
            },
        )

        assert response.status_code == 201

        assert response.data["email"] == "test@gmail.com"

    def test_non_admin_can_create_user(self):

        self.client = APIClient()

        admin = UserFactory(is_admin=False)

        self.client.force_authenticate(user=admin)

        response = self.client.post(
            "/api/users/",
            data={
                "email": "test@gmail.com",
                "first_name": "lion",
                "last_name": "lion",
                "gender": "male",
            },
        )

        assert response.status_code == 403

    def test_admin_can_update_user(self):

        self.client = APIClient()

        admin = UserFactory(is_admin=True)

        user = UserFactory(is_admin=False)

        self.client.force_authenticate(user=admin)

        response = self.client.patch(
            f"/api/users/{user.id}/", data={"first_name": "tiger"}, format="multipart"
        )

        assert response.status_code == 200

        assert response.data["first_name"] == "tiger"

    @pytest.mark.django_db
    def test_admin_can_delete_user(self):

        self.client = APIClient()

        admin = UserFactory(is_admin=True)

        user = UserFactory()

        self.client.force_authenticate(user=admin)

        response = self.client.delete(f"/api/users/{user.id}/")

        assert response.status_code == 204

    def test_view_filtering_by_country_and_gender(self):

        self.client = APIClient()

        target_user = UserFactory(country="Lebanon", gender="Female")
        UserFactory(country="Canada", gender="male")

        response = self.client.get("/api/list/?country=Lebanon&gender=Female)")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["email"] == target_user.email
