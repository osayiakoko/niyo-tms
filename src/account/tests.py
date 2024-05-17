from rest_framework import status
from rest_framework.test import APIClient


def test_user_details_view(api_client_jwt: APIClient):
    url = "/v1/account/me"

    res = api_client_jwt.get(url)
    assert res.status_code == status.HTTP_200_OK

    expected_keys = [
        "id",
        "first_name",
        "last_name",
        "email",
    ]
    assert all(key in res.data for key in expected_keys)


def test_users_list_view(api_client_jwt: APIClient):
    url = "/v1/account/users"

    res = api_client_jwt.get(url)
    assert res.status_code == status.HTTP_200_OK

    assert isinstance(res.data, list)

    expected_keys = [
        "id",
        "first_name",
        "last_name",
        "email",
    ]
    assert all(key in res.data[0] for key in expected_keys)
