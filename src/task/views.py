# views.py
from rest_framework import viewsets, status

from core.exceptions import APIException

from .enums import TaskWebSocketEvent
from .models import Task
from .permissions import TaskPermission
from .serializers import TaskSerializer
from .utils import notify_task_listeners


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [TaskPermission]

    def perform_create(self, serializer):
        # Attach the 'created_by' field to the user making the request
        serializer.save(created_by=self.request.user)
        notify_task_listeners(TaskWebSocketEvent.CREATE, serializer.data)

    def perform_update(self, serializer):
        # Check if it's a partial update (PATCH request) by assigned user
        if serializer.partial and self.request.user == serializer.instance.assigned_to:
            data = serializer.validated_data
            # Check if other fields apart from 'status' field is being updated
            if not (len(data) == 1 and "status" in data):
                raise APIException(
                    detail="You can only update the status of the task.",
                    status_code=status.HTTP_403_FORBIDDEN,
                )

        serializer.save()
        notify_task_listeners(TaskWebSocketEvent.UPDATE, serializer.data)

    def perform_destroy(self, instance):
        task_id = instance.id
        instance.delete()
        notify_task_listeners(TaskWebSocketEvent.DELETE, {"id": task_id})
