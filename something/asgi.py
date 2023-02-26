"""
ASGI config for testchannel project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "something.settings")

import django
django.setup()


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import realtime.routing
from realtime.channel_middleware import TokenAuthMiddleware


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # Just HTTP for now. (We can add other protocols later.)
        # "websocket": AllowedHostsOriginValidator(
        #     # AuthMiddlewareStack(URLRouter(realtime.routing.websocket_urlpatterns))
        #     AuthMiddlewareStack(URLRouter(realtime.routing.websocket_urlpatterns))
        # ),
        "websocket": AllowedHostsOriginValidator(
            # AuthMiddlewareStack(URLRouter(realtime.routing.websocket_urlpatterns))
            TokenAuthMiddleware(URLRouter(realtime.routing.websocket_urlpatterns))
        ),
    }
)