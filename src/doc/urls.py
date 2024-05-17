from django.conf import settings
from django.urls import path

from core.enums import ProjectEnv
from .views import root_redirect, health_check

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


app_name = "doc"

urlpatterns = [
    path("health-check", health_check),
]

if settings.PROJECT_ENV == ProjectEnv.DEVELOPMENT:
    urlpatterns += [
        path("schema", SpectacularAPIView.as_view(), name="schema"),
        # Optional UI:
        path(
            "swagger-ui",
            SpectacularSwaggerView.as_view(url_name="doc:schema"),
            name="swagger-ui",
        ),
        path(
            "redoc", SpectacularRedocView.as_view(url_name="doc:schema"), name="redoc"
        ),
        path("", root_redirect),
    ]
