import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_login_view(api_client: APIClient):
    url = "/v1/auth/login"
    email = "johndoe@gmail.com"
    password = "pass1234"

    user = baker.make("account.User", email=email)
    user.set_password(password)
    user.save()

    data = {"email": email, "password": password}
    res = api_client.post(url, data)
    assert res.status_code == status.HTTP_200_OK

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
