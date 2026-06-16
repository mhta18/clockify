from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, UserListAPIView

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
BASE_NAME = "users"
urlpatterns = [
    path(
        f"{BASE_NAME}/list/",
        UserListAPIView.as_view(),
        name="user-list",
    ),
    path("", include(router.urls)),
    path(
        f"{BASE_NAME}/list/export/",
        UserListAPIView.as_view(),
        name="user-export",
    ),
]
