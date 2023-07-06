from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chatroom/(?P<room_id>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/notification/", consumers.NotificationConsumer.as_asgi()),
]
