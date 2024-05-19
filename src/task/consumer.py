from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .constant import TASK_CHANNEL_GROUP_NAME


class TaskConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.channel_group_name = TASK_CHANNEL_GROUP_NAME

        # Join task group
        await self.channel_layer.group_add(self.channel_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, _):
        await self.channel_layer.group_discard(
            self.channel_group_name, self.channel_name
        )

    async def notify(self, event: dict):
        # Send message to WebSocket
        await self.send_json(event["message"])
