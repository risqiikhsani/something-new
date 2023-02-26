from django.contrib import admin

from .models import ChatRoom, GroupChatRoom, Chat, Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'channel_name', 'server')
    list_filter = ('user',)



@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'time_creation')
    list_filter = ('time_creation',)
    raw_id_fields = ('user',)


@admin.register(GroupChatRoom)
class GroupChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_creation', 'generated_link')
    list_filter = ('time_creation',)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sender',
        'text',
        'time_creation',
        'time_update',
        'forwarded',
        'reply_from',
    )
    list_filter = (
        'sender',
        'time_creation',
        'time_update',
        'forwarded',
        'reply_from',
    )
    raw_id_fields = ('room',)