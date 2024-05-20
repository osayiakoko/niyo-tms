import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_view(api_client: APIClient):
    url = "/v1/auth/register"
    first_name = "John"
    last_name = "Doe"
    email = "johndoe@gmail.com"
    password = "Pass1234"

    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
    }
    res = api_client.post(url, data)
    assert res.status_code == status.HTTP_201_CREATED

    expected_keys = [
        "id",
        "first_name",
        "last_name",
        "email",
        "token",
    ]
    assert all(key in res.data for key in expected_keys)

    expected_keys = ["access", "refresh"]
    assert all(key in res.data["token"] for key in expected_keys)
