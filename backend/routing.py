# mysite/routing.py

from chat.routing import websocket_urlpatterns
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import URLRouter

from django.urls import path

route_patterns = AllowedHostsOriginValidator(
    URLRouter([
        path('', URLRouter(websocket_urlpatterns))
    ])
)
