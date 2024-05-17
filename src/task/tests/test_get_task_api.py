import pytest
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker

from account.models import User
from ..models import Task
from ..serializers import TaskSerializer


def _test_passed(api_client, user_admin, user) -> bool:

    # Create some tasks
    tasks: list[Task] = baker.make(
        "task.Task", _quantity=3, created_by=user_admin, assigned_to=user
    )

    url = "/v1/tasks/"
    res = api_client.get(url)

    success = res.status_code == status.HTTP_200_OK

    # Deserialize response data
    serializer = TaskSerializer(tasks, many=True)
    expected_data = serializer.data

    # Compare the retrieved data with the expected data
    is_expected_data = res.data == expected_data
    return success and is_expected_data


@pytest.mark.django_db
def test_get_tasks_by_admin(
    api_client_jwt_admin: APIClient, user_admin: User, user: User
):
    assert _test_passed(api_client_jwt_admin, user_admin, user)


@pytest.mark.django_db
def test_get_tasks_by_user(api_client_jwt: APIClient, user_admin: User, user: User):

    assert _test_passed(api_client_jwt, user_admin, user)
