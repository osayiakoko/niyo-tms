import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone

from account.models import User


def _task_data(user_id) -> dict:
    return {
        "title": "Test Task",
        "description": "Test task description",
        "priority": "high",
        "status": "todo",
        "assigned_to": user_id,
        "due_at": timezone.now() + timezone.timedelta(days=1),
    }


@pytest.mark.django_db
def test_create_task_by_admin(api_client_jwt_admin: APIClient, user: User):
    url = "/v1/tasks/"

    data = _task_data(user.id)
    res = api_client_jwt_admin.post(url, data)

    assert res.status_code == status.HTTP_201_CREATED

    expected_keys = [
        "id",
        "title",
        "description",
        "priority",
        "status",
        "created_at",
        "updated_at",
        "due_at",
        "created_by",
        "assigned_to",
    ]
    assert all(key in res.data for key in expected_keys)


@pytest.mark.django_db
def test_create_task_by_user_fails(api_client_jwt: APIClient, user_admin: User):
    url = "/v1/tasks/"

    data = _task_data(user_admin.id)
    res = api_client_jwt.post(url, data)

    assert res.status_code == status.HTTP_403_FORBIDDEN
