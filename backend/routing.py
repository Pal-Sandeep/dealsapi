# mysite/routing.py

from chat import routing
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import URLRouter

from django.urls import path

route_patterns = AllowedHostsOriginValidator(
    URLRouter([
        path('', URLRouter(
            routing.websocket_urlpatterns))
    ])
)
