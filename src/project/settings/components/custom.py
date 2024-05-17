# pylint: disable=E0602,C0114

SUPERUSER_USERNAME = env("DJANGO_SUPERUSER_EMAIL")  # noqa: F821 # type: ignore
SUPERUSER_PASSWORD = env("DJANGO_SUPERUSER_PASSWORD")  # noqa: F821 # type: ignore
