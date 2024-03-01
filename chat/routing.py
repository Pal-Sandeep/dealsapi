from django.urls import path
from chat import consumers

websocket_urlpatterns = [
    path(
        # '/ws/users/<int:userId>/chat/',
        '<int:userId>',
        consumers.ChatConsumer.as_asgi()
    ),
]
