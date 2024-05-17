import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from .constants import (
    TEST_ADMIN_USER_EMAIL,
    TEST_ADMIN_USER_PASSWORD,
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
)


def _get_access_token(api_client, user, isAdmin=False):
    url = "/v1/auth/login"
    data = {
        "email": str(user.email),
        "password": TEST_ADMIN_USER_PASSWORD if isAdmin else TEST_USER_PASSWORD,
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK, "Login failed during test setup"
    return response.data["token"]["access"]


@pytest.fixture
def api_client() -> APIClient:
    api_client = APIClient()
    return api_client


@pytest.fixture
def api_client_jwt(api_client, user) -> APIClient:
    token = _get_access_token(api_client, user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture
def api_client_jwt_admin(api_client, user_admin) -> APIClient:
    token = _get_access_token(api_client, user_admin, isAdmin=True)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture()
def user(db):
    user = baker.make("account.User", email=TEST_USER_EMAIL)
    user.set_password(TEST_USER_PASSWORD)
    user.save()
    return user


@pytest.fixture()
def user_admin(db):
    user = baker.make("account.User", email=TEST_ADMIN_USER_EMAIL, is_staff=True)
    user.set_password(TEST_ADMIN_USER_PASSWORD)
    user.save()
    return user
