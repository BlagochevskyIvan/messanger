from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('conf/<str:conf_name>', consumers.ChatConsumer.as_asgi()),
]