import pytest

from rest_framework.test import APIClient
from freezegun import freeze_time
from users.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserViewSet:

    def setup_method(self):
        self.client = APIClient()

    def test_admin_can_list_users(self):

        admin_user = UserFactory(is_admin=True)

        UserFactory.create_batch(3)

        self.client.force_authenticate(user=admin_user)

        response = self.client.get("/api/users/list/")

        assert response.status_code == 200

        assert len(response.data) >= 3

    def test_non_admin_cannot_list_users(self):

        self.client = APIClient()

        user = UserFactory(is_admin=False)

        self.client.force_authenticate(user=user)

        response = self.client.get("/api/users/list/")

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

    def test_non_admin_cannot_create_user(self):

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

    # filtering tests----------------------------------------------------------------------------------------------

    def test_filter_by_gender(self):
        admin = UserFactory(is_admin=True, gender="male")
        self.client.force_authenticate(user=admin)

        UserFactory(gender="female")
        UserFactory(gender="male")

        response = self.client.get("/api/users/list/?gender=female")

        assert response.status_code == 200
        assert len(response.data) == 1

    def test_view_filtering_by_country(self):
        admin = UserFactory(is_admin=True, country="canada")
        self.client.force_authenticate(user=admin)

        UserFactory(country="lebanon")
        UserFactory(country="canada")

        response = self.client.get("/api/users/list/?country=lebanon")

        assert response.status_code == 200
        assert len(response.data) == 1

    def test_view_filtering_by_created_at(self):
        self.client = APIClient()

        with freeze_time("2026-05-16 12:00:00"):
            admin = UserFactory(is_admin=True,email="user1@gmail.com")
            self.client.force_authenticate(user=admin)

        UserFactory(email="user3@gmail.com")

        response = self.client.get(
            "/api/users/list/", {"created_at": "2026-05-16 12:00:00"}
        )

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["email"] == admin.email

    # # ordering tests----------------------------------------------------------------------------------------------
    def test_view_ordering_by_counrty(self):
        self.client = APIClient()
        admin = UserFactory(is_admin=True, country="iran")
        self.client.force_authenticate(user=admin)

        UserFactory(country="lebanon")
        UserFactory(country="canada")

        response = self.client.get("/api/users/list/?ordering=country")

        assert response.status_code == 200
        assert response.data[0]["country"] == "canada"

    def test_view_ordering_by_first_name(self):
        self.client = APIClient()
        admin = UserFactory(is_admin=True, first_name="Aria")
        self.client.force_authenticate(user=admin)

        UserFactory(first_name="Lion")
        UserFactory(first_name="Tiger")

        response = self.client.get("/api/users/list/?ordering=first_name")

        assert response.status_code == 200
        assert response.data[0]["first_name"] == "Aria"

    def test_view_ordering_by_last_name(self):
        self.client = APIClient()
        admin = UserFactory(is_admin=True, last_name="Barton")
        self.client.force_authenticate(user=admin)

        UserFactory(last_name="Lion")
        UserFactory(last_name="Tiger")

        response = self.client.get("/api/users/list/?ordering=last_name")

        assert response.status_code == 200
        assert response.data[0]["last_name"] == "Barton"

    def test_created_at_ordering(self):
        self.client = APIClient()
        with freeze_time("2026-05-14 12:00:00"):
            admin = UserFactory(is_admin=True,email="user0@gmail.com")

        self.client.force_authenticate(user=admin)
        with freeze_time("2026-05-15 12:00:00"):
            old_user = UserFactory(email="user1@gmail.com")

        with freeze_time("2026-05-16 12:00:00"):
            new_user = UserFactory(email="user2@gmail.com")

        response = self.client.get("/api/users/list/", {"ordering": "created_at"})

        assert response.status_code == 200
        assert response.data[0]["email"] == admin.email
        assert response.data[1]["email"] == old_user.email
        assert response.data[2]["email"] == new_user.email

    # # searching tests----------------------------------------------------------------------------------------------
    def test_view_searching_by_email(self):
        self.client = APIClient()
        admin = UserFactory(is_admin=True,email="admin@gmail.com")
        self.client.force_authenticate(user=admin)

        target_user = UserFactory(email="mahta.m.1183@gmail.com")
        UserFactory(email="user@gmail.com")
        response = self.client.get(f"/api/users/list/?search={target_user.email}")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["email"] == target_user.email

    def test_view_searching_by_first_name(self):
        self.client = APIClient()
        admin = UserFactory(is_admin=True,first_name = "leva")
        self.client.force_authenticate(user=admin)

        target_user = UserFactory(first_name="mahta")
        UserFactory(first_name="another")
        response = self.client.get(f"/api/users/list/?search={target_user.first_name}")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["first_name"] == target_user.first_name
