from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ReportsViewSet

router = DefaultRouter()
router.register(r'admin-dashbord',ReportsViewSet,basename='admin-dashbord')

urlpatterns = [
    path('',include(router.urls))
]