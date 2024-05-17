from rest_framework import status
from rest_framework.test import APIClient


def test_refresh_token_view(api_client: APIClient, user):
    url = "/v1/auth/refresh-token"
    refresh_token = user.token["refresh"]
    data = {"refresh_token": refresh_token}

    res = api_client.post(url, data)
    assert res.status_code == status.HTTP_200_OK

    expected_keys = [
        "access_token",
    ]
    assert all(key in res.data for key in expected_keys)
