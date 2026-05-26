from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FreelancerListAPiView,
    EmployerListAPIView,
    FreelancerViewSet,
    EmployerViewSet,
)

router = DefaultRouter()

router.register(r"freelancers", FreelancerViewSet, basename="freelancer")
router.register(r"employers", EmployerViewSet, basename="employer")

urlpatterns = [
    path(
        "freelancers/list/",
        FreelancerListAPiView.as_view(),
        name="freelancer-list",
    ),
    path(
        "employers/list/",
        EmployerListAPIView.as_view(),
        name="employer-list",
    ),
    path("", include(router.urls)),
]
