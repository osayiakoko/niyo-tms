# admin.py
from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_by",
        "assigned_to",
        "due_at",
        "priority",
        "status",
    )
    list_filter = (
        "created_by",
        "assigned_to",
        "created_at",
        "due_at",
        "priority",
        "status",
    )
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("title",)
