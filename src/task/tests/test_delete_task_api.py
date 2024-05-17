import pytest
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker

from account.models import User
from ..models import Task


@pytest.mark.django_db
def test_delete_task_by_admin(
    api_client_jwt_admin: APIClient, user: User, user_admin: User
):
    # Create a task created by the admin user
    task: Task = baker.make("task.Task", created_by=user_admin, assigned_to=user)

    url = f"/v1/tasks/{task.id}/"
    res = api_client_jwt_admin.delete(url)

    assert res.status_code == status.HTTP_204_NO_CONTENT

    # Verify that the task has been deleted
    with pytest.raises(Task.DoesNotExist):
        Task.objects.get(id=task.id)


@pytest.mark.django_db
def test_delete_task_by_another_admin_fails(
    api_client_jwt_admin: APIClient, user: User
):
    # Create a task created by another admin user
    another_admin_user = baker.make("account.User", is_staff=True)
    task: Task = baker.make(
        "task.Task", created_by=another_admin_user, assigned_to=user
    )

    url = f"/v1/tasks/{task.id}/"
    res = api_client_jwt_admin.delete(url)

    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Verify that the task still exists
    assert Task.objects.filter(id=task.id).exists()


@pytest.mark.django_db
def test_delete_task_by_user_fails(
    api_client_jwt: APIClient, user_admin: User, user: User
):
    # Create a task created by the admin user
    task: Task = baker.make("task.Task", created_by=user_admin, assigned_to=user)

    url = f"/v1/tasks/{task.id}/"
    res = api_client_jwt.delete(url)

    assert res.status_code == status.HTTP_403_FORBIDDEN

    # Verify that the task still exists
    assert Task.objects.filter(id=task.id).exists()
