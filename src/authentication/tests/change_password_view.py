from rest_framework import status
from rest_framework.test import APIClient

from core.tests.constants import TEST_USER_PASSWORD


def _make_request(api_client_jwt: APIClient, data: dict):
    url = "/v1/auth/change-password"
    return api_client_jwt.post(url, data)


def test_change_password_view_success(api_client_jwt: APIClient):
    data = {
        "old_password": TEST_USER_PASSWORD,
        "new_password": "Pass!1!1",
    }

    res = _make_request(api_client_jwt, data)
    assert res.status_code == status.HTTP_200_OK


def test_change_password_view_same_password(api_client_jwt: APIClient):
    data = {
        "old_password": TEST_USER_PASSWORD,
        "new_password": TEST_USER_PASSWORD,
    }

    res = _make_request(api_client_jwt, data)
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_change_password_view_wrong_password(api_client_jwt: APIClient):
    data = {
        "old_password": "wrong_password",
        "new_password": TEST_USER_PASSWORD,
    }

    res = _make_request(api_client_jwt, data)
    assert res.status_code == status.HTTP_400_BAD_REQUEST
