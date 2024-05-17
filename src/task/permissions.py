from rest_framework import permissions


class TaskPermission(permissions.BasePermission):
    """
    Custom permission to allow users to update status of tasks assigned to them
    and admins to create tasks, update and delete any task.
    """

    def has_permission(self, request, view):
        if view.action == "create":
            # Only allow admins to create tasks
            return request.user and request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        if view.action == "partial_update":
            # Allow admins to partially update tasks created by them
            if request.user.is_staff and obj.created_by == request.user:
                return True
            # Allow users to partially update tasks assigned to them
            elif obj.assigned_to == request.user:
                return True
            return False

        # Allow admins to update or delete tasks created by them
        elif view.action in ["update", "destroy"]:
            return (
                request.user
                and request.user.is_staff
                and obj.created_by == request.user
            )

        return True
