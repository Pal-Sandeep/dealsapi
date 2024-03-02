from django.urls import path
from chat import consumers

websocket_urlpatterns = [
    path(
        '<int:userId>',
        consumers.ChatConsumer.as_asgi()
    ),
]
