from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path("ws/chat/public_room/", consumers.ChatConsumer.as_asgi()),
]
