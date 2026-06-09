from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.urls import include
from django.conf.urls.i18n import set_language
from django.views.generic import TemplateView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


BASE_NAME = "api/"
urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", set_language, name="set_language"),
    path(BASE_NAME, include("users.urls")),
    path(BASE_NAME, include("authentication.urls")),
    path(BASE_NAME, include("teams.urls")),
    path(BASE_NAME, include("projects.urls")),
    path(BASE_NAME, include("contracts.urls")),
    path(BASE_NAME, include("timetracking.urls")),
    path(BASE_NAME, include("reports.urls")),
    path(BASE_NAME, include("notifications.urls")),
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "swagger-test/",
        TemplateView.as_view(template_name="swagger_dark.html"),
    ),
]


urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
