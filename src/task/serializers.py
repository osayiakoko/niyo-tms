# serializers.py
from django.utils import timezone
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        read_only_fields = (
            "id",
            "created_by",
        )
        fields = "__all__"

    def validate_due_at(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Due at cannot be in the past.")
        return value
