from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.mail import send_mail
from django.conf import settings
from .helpers import get_random_alphanumeric_string
from .models import *
from django.db.models.signals import post_save, m2m_changed, post_delete
import json
from django.contrib.auth import get_user_model
User = get_user_model()


# https://techincent.com/how-to-delete-file-when-models-instance-is-delete-or-update-in-django/
# or
# https://djangosnippets.org/snippets/10638/


def auto_clear_files_on_delete(sender, instance, *args, **kwargs):
    print("file handler signal is running")
    # delete filtered and sized cache images
    instance.image.delete_all_created_images()
    try:
        # delete original image
        instance.image.delete(save=False)
    except:
        pass


post_delete.connect(auto_clear_files_on_delete,
                    sender=PostMedia, dispatch_uid="unique")


@database_sync_to_async
def get_channel_name(a):
    return a.channel_name


# def chat_message(event):
#     print("send notification running")
#     channel_layer = get_channel_layer()
#     # Send message to WebSocket
#     async_to_sync(channel_layer.send)(text_data=json.dumps({
#         "text": event["text"],
#         "type": "app_notification",
#     }))


def LikeNotification(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    print("like notification signal")
    user = None
    obj = None
    event = None
    if instance.post:
        user = instance.post.user
        obj = instance.post.id
        event = "liked_post"
    elif instance.comment:
        user = instance.comment.user
        obj = instance.comment.id
        event = "liked_comment"
    elif instance.reply:
        user = instance.reply.user
        obj = instance.reply.id
        event = "liked_reply"
    else:
        return None

    if created:
        print("like notification signal is running")
        print(user)
        # if user.client_set.all().filter(server="app_notification").exists():
        #     for a in user.client_set.all().filter(server="app_notification"):
        #         print(a.channel_name)
        #         async_to_sync(channel_layer.send(str(a.channel_name), {
        #             "type": "send_notification",
        #             "text": {
        #                 "event": str(event),
        #                 "sender": str(instance.user.id),
        #                 "object": str(obj)
        #             },
        #         }))
        group_name = "notification_%s" % user.id
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_notification',
                "text": "hello"
            }
        )
                


post_save.connect(LikeNotification, sender=Like, dispatch_uid="unique")
