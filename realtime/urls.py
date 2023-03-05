from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    NotificationList,
    ChatRoomList,
    GetOrCreateChatRoom,
)

urlpatterns = [

    path('notifications',NotificationList.as_view(), name='notification-list'),
    path('chatrooms',ChatRoomList.as_view(), name='chatroom-list'),
    path('get_or_create_twoperson_chatroom/<int:user_id>',GetOrCreateChatRoom.as_view(), name='get_create_chatroom'),
    

]