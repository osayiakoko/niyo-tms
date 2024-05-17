# models.py
from django.db import models

from .choices import TaskPriority, TaskStatus


class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_by = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="tasks_created",
    )
    assigned_to = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="tasks_assigned",
        null=True,
        blank=True,
    )
    priority = models.CharField(
        max_length=30, choices=TaskPriority.choices, default=TaskPriority.LOW
    )
    status = models.CharField(
        max_length=30, choices=TaskStatus.choices, default=TaskStatus.TODO
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    due_date = models.DateField()

    class Meta:
        db_table = "task"

    def __str__(self):
        return self.title
