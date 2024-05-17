from django.db.models import TextChoices


class TaskStatus(TextChoices):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(TextChoices):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
