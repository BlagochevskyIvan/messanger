"""
ASGI config for siteproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from chat_app import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtime_messanger.settings')
django_asgi_app = get_asgi_application()

from chat_app import routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ))
})
