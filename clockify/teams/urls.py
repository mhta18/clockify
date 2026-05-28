from django.urls import path,include
from rest_framework .routers import DefaultRouter   
from .views import TeamViewSet,TaskViewSet

router =DefaultRouter()
router.register(r'teams', TeamViewSet, basename='teams')
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
]