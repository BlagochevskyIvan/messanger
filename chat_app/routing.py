from django.urls import path, re_path
from . import consumers


websocket_urlpatterns = [
    # re_path(r"ws/conf/(?P<conf_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/conf/test/$", consumers.ChatConsumer.as_asgi()),
]