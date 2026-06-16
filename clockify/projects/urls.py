from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjctViewSet, ProjctListAPIView

router = DefaultRouter()
router.register(r"projects", ProjctViewSet, basename="projects")
BASE_NAME = "projects"
urlpatterns = [
    path(
        f"{BASE_NAME}/list/",
        ProjctListAPIView.as_view(),
        name="project-list",
    ),
    path("", include(router.urls)),
]
