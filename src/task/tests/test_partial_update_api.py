import pytest
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker

from account.models import User
from ..models import Task
from ..choices import TaskStatus


@pytest.mark.django_db
def test_partial_update_task_by_admin(
    api_client_jwt_admin: APIClient, user: User, user_admin: User
):
    # Create a task created by the admin user
    task: Task = baker.make("task.Task", created_by=user_admin, assigned_to=user)

    url = f"/v1/tasks/{task.id}/"
    update_data = {"title": "Updated Title"}
    res = api_client_jwt_admin.patch(url, update_data)

    assert res.status_code == status.HTTP_200_OK
    # Verify that the task has been partially updated
    task.refresh_from_db()
    assert task.title == update_data["title"]


@pytest.mark.django_db
def test_partial_update_task_by_another_admin_fails(
    api_client_jwt_admin: APIClient, user: User
):
    # Create a task created by another admin user
    another_admin_user = baker.make("account.User", is_staff=True)
    task: Task = baker.make(
        "task.Task", created_by=another_admin_user, assigned_to=user
    )

    url = f"/v1/tasks/{task.id}/"
    update_data = {"title": "Updated Title"}
    res = api_client_jwt_admin.patch(url, update_data)

    assert res.status_code == status.HTTP_403_FORBIDDEN
    # Verify that the task title remains unchanged
    task.refresh_from_db()
    assert task.title != update_data["title"]


@pytest.mark.django_db
def test_partial_update_task_status_by_assigned_user(
    api_client_jwt: APIClient, user_admin: User, user: User
):
    # Create a task created by the admin user
    task: Task = baker.make("task.Task", created_by=user_admin, assigned_to=user)

    url = f"/v1/tasks/{task.id}/"
    update_data = {"status": "done"}
    res = api_client_jwt.patch(url, update_data)

    assert res.status_code == status.HTTP_200_OK
    # Verify that the task status changed
    task.refresh_from_db()
    assert task.status == TaskStatus.DONE


@pytest.mark.django_db
def test_partial_update_task_title_by_assigned_user_fails(
    api_client_jwt: APIClient, user_admin: User, user: User
):
    # Create a task created by the admin user
    task: Task = baker.make("task.Task", created_by=user_admin, assigned_to=user)

    url = f"/v1/tasks/{task.id}/"
    update_data = {"title": "Updated Title"}
    res = api_client_jwt.patch(url, update_data)

    assert res.status_code == status.HTTP_403_FORBIDDEN
    # Verify that the task title remains unchanged
    task.refresh_from_db()
    assert task.title != update_data["title"]
