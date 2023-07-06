from django.contrib import admin

from .models import *

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'event',
        'sender_id',
        'subject_data',
        'subject_id',
        'subject_text_preview',
        'object_data',
        'object_id',
        'object_text_preview',
        'time_creation',
    )
    list_filter = ('user', 'time_creation')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'channel_name', 'server')
    list_filter = ('user',)

@admin.register(ClientSocketData)
class ClientSocketDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'last_read_id_in_server', 'server_name')
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
