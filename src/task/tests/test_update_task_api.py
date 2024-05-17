import pytest
from django.utils import timezone
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from account.models import User
from ..models import Task


def _task_data(user) -> dict:
    return {
        "title": "Test Task",
        "description": "Test task description",
        "priority": "high",
        "status": "todo",
        "assigned_to": user,
        "due_at": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
    }


def _updated_task_data(user) -> dict:
    return {
        "title": "Updated Test Task",
        "description": "Updated test task description",
        "priority": "medium",
        "status": "in_progress",
        "assigned_to": user,
        "due_at": (timezone.now() + timezone.timedelta(days=2)).isoformat(),
    }


@pytest.mark.django_db
def test_update_task_by_admin(
    api_client_jwt_admin: APIClient, user: User, user_admin: User
):
    # Create a task created by the admin user
    task: Task = baker.make("task.Task", created_by=user_admin, **_task_data(user))

    url = f"/v1/tasks/{task.id}/"
    update_data = _updated_task_data(task.assigned_to)

    update_res = api_client_jwt_admin.put(url, update_data)
    assert update_res.status_code == status.HTTP_200_OK

    # Verify that the update was successful
    updated_task_data = update_res.data
    assert updated_task_data["title"] == update_data["title"]
    assert updated_task_data["description"] == update_data["description"]
    assert updated_task_data["priority"] == update_data["priority"]
    assert updated_task_data["status"] == update_data["status"]
    assert updated_task_data["due_at"] == update_data["due_at"].replace("+00:00", "Z")


@pytest.mark.django_db
def test_update_task_by_another_admin_fails(
    api_client_jwt_admin: APIClient, user: User
):
    # Create a task created by another admin user
    another_admin_user = baker.make("account.User", is_staff=True)
    task: Task = baker.make(
        "task.Task", created_by=another_admin_user, **_task_data(user)
    )

    url = f"/v1/tasks/{task.id}/"
    update_data = _updated_task_data(task.assigned_to)
    res = api_client_jwt_admin.put(url, update_data)

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_task_by_user_fails(
    api_client_jwt: APIClient, user_admin: User, user: User
):
    # Create a task created by the admin user
    task: Task = baker.make("task.Task", created_by=user_admin, **_task_data(user))

    url = f"/v1/tasks/{task.id}/"
    update_data = _updated_task_data(task.assigned_to)
    res = api_client_jwt.put(url, update_data)

    assert res.status_code == status.HTTP_403_FORBIDDEN
