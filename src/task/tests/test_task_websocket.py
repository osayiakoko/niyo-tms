import pytest
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator

from ..consumer import TaskConsumer


task_data = {
    "event": "create",
    "payload": {
        "id": 1,
        "title": "Test title",
        "description": "Test description",
        "priority": "high",
        "status": "todo",
        "created_at": "2024-05-19T15:52:43.389788Z",
        "updated_at": "2024-05-19T17:20:43.908888Z",
        "due_at": "2024-05-20T12:00:00Z",
        "created_by": 1,
        "assigned_to": 2,
    },
}


@pytest.mark.asyncio
async def test_task_websocket():
    # Create a test instance of the channel layer
    channel_layer = get_channel_layer()

    # Instantiate the consumer
    communicator = WebsocketCommunicator(TaskConsumer.as_asgi(), "GET", "/ws/v1/tasks/")

    # Set up communication with the consumer
    connected, _ = await communicator.connect()

    # Assert that the connection was successful
    assert connected

    try:
        # Send a message to the consumer
        channel_group_name = "task"
        await channel_layer.group_send(
            channel_group_name, {"type": "notify", "message": task_data}
        )

        # Receive the message from the consumer
        response = await communicator.receive_json_from()

        # Assert that the message received matches what was expected
        assert response == task_data

    finally:
        # Disconnect from the consumer
        await communicator.disconnect()
