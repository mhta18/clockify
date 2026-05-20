from  rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.renderers import JSONRenderer
from .views import UserViewSet,UserListAPIView

router = DefaultRouter()
router.register("users", UserViewSet, basename='users')

urlpatterns = [
    path(
        "list/",
        UserListAPIView.as_view(),
        name="user-list",
    ),
    path("", include(router.urls)),
    path(
        "list/export/",
        UserListAPIView.as_view(),
        name="user-export",
    ),
]
