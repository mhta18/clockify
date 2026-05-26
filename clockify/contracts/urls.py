from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FreelancerContractListAPiView,
    EmployerContractListAPIView,
    FreelancerContractViewSet,
    EmployerContractViewSet,
)

router = DefaultRouter()

router.register(r"freelancers", FreelancerContractViewSet, basename="freelancers")
router.register(r"employers", EmployerContractViewSet, basename="employers")

urlpatterns = [
    path(
        "freelancers/list/",
        FreelancerContractListAPiView.as_view(),
        name="freelancer-list",
    ),
    path(
        "employers/list/",
        EmployerContractListAPIView.as_view(),
        name="employer-list",
    ),
    path("", include(router.urls)),
]
