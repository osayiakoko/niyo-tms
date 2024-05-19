from asgiref.sync import async_to_sync
import channels.layers

from .constant import TASK_CHANNEL_GROUP_NAME
from .enums import TaskWebSocketEvent


def notify_task_listeners(event: TaskWebSocketEvent, payload: dict) -> None:
    channel_group_name = TASK_CHANNEL_GROUP_NAME
    message = {
        "event": event.value,
        "payload": payload,
    }

    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        channel_group_name, {"type": "notify", "message": message}
    )
