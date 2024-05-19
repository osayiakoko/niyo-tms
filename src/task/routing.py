# chat/routing.py
from django.urls import re_path

from .consumer import TaskConsumer

websocket_urlpatterns = [
    re_path(r"ws/v1/tasks/$", TaskConsumer.as_asgi()),
]
