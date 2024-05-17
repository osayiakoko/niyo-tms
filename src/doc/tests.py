from rest_framework import status
from rest_framework.test import APIClient


def test_health_check_view(api_client: APIClient):
    url = "/health-check"

    res = api_client.get(url)
    assert res.status_code == status.HTTP_200_OK
