import chat.routing
import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from .routing import route_patterns

from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": route_patterns,
    # Just HTTP for now. (We can add other protocols later.)
})
