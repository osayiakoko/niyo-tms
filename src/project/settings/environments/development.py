# pylint: skip-file
from core.enums import ProjectEnv


PROJECT_ENV = ProjectEnv.DEVELOPMENT
DEBUG = True
ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = []

# CORS SETTING
CORS_ALLOW_ALL_ORIGINS = True

#  REST FRAMEWORK SETTINGS
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(  # noqa: F821 # type: ignore
    "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer"
)
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].append(  # noqa: F821 # type: ignore
    "rest_framework.authentication.SessionAuthentication"
)
