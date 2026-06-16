from django.urls import path
from .views import NotificationMarkReadAPIView

urlpatterns = [
    path(
        "notifications/mark-read/",
        NotificationMarkReadAPIView.as_view(),
        name="notification-mark-all-read",
    ),
    path(
        "notifications/mark-read/<int:pk>/",
        NotificationMarkReadAPIView.as_view(),
        name="notification-mark-single-read",
    ),
]
