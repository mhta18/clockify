from django.urls import path,include
from rest_framework .routers import DefaultRouter   
from .views import TeamViewSet,TaskViewSet,TaskListAPIView

router =DefaultRouter()
router.register(r'teams', TeamViewSet, basename='teams')
router.register(r"supervisor/tasks", TaskViewSet  , basename="supervisor-task")
BASE_NAME = "my-tasks"
urlpatterns = [
    path(
        f"{BASE_NAME}/list/",
        TaskListAPIView.as_view(),
        name="my-task-list",
    ),
    path("", include(router.urls)),
]
