from enum import Enum


class TaskWebSocketEvent(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
