from django.urls import path,include
from rest_framework .routers import DefaultRouter   
from .views import TeamViewSet,TaskViewSet

router =DefaultRouter()
router.register(r'teams', TeamViewSet, basename='teams')
router.register(r"my-tasks", TaskViewSet, basename="my-task")
router.register(r"supervisor/tasks", TaskViewSet, basename="supervisor-task")
urlpatterns = [
    path('', include(router.urls)),
]
