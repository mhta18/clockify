from  rest_framework.routers import DefaultRouter
from django.urls import path, include
from drf_excel.renderers import XLSXRenderer
from .views import UserViewSet,UserListAPIView

router = DefaultRouter()
router.register("users", UserViewSet, basename='users')

urlpatterns = [
 path("list/", UserListAPIView.as_view(), name="user-list"),
 path("", include(router.urls)),
 path("users/export/", UserListAPIView.as_view(renderer_classes=[XLSXRenderer]), name="user-export"),
]
