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

from realtime.models import *

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
    event = None
    obj_data = None
    obj = None
    if instance.post:
        user = instance.post.user
        event = "liked_post"
        obj_data = "post"
        obj = instance.post
    elif instance.comment:
        user = instance.comment.user
        event = "liked_comment"
        obj_data = "comment"
        obj = instance.comment
    elif instance.reply:
        user = instance.reply.user
        event = "liked_reply"
        obj_data = "reply"
        obj = instance.reply
    else:
        return None

    if created and user.id is not instance.user.id: 
        print("like notification signal is running")
        Notification.objects.create(
            user=user,
            event=str(event),
            sender_id=instance.user.id,
            subject_data = "like",
            subject_id = instance.id,
            object_data = str(obj_data),
            object_id=obj.id,
            object_text_preview=str(obj.text),
        )
        group_name = "notification_%s" % user.id
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'app_notification',
                "data": {
                    "event": str(event),
                    "sender_id": instance.user.id,
                    "sender_name":str(instance.user.profile.name),
                    "subject_data":"like",
                    "subject_id":instance.id,
                    "object_data": str(obj_data),
                    "object_id": obj.id,
                },
            }
        )


post_save.connect(LikeNotification, sender=Like, dispatch_uid="unique")

def CommentNotification(sender,instance,created,**kwargs):
    channel_layer = get_channel_layer()
    user = instance.post.user
    event = "commented_post"
    obj = instance.post
    if created and user.id is not instance.user.id:
        Notification.objects.create(
            user=user,
            event=str(event),
            sender_id=instance.user.id,
            subject_data = "comment",
            subject_id = instance.id,
            subject_text_preview=str(instance.text),
            object_data = "post",
            object_id=obj.id,
            object_text_preview=str(obj.text),
        )
        group_name = "notification_%s" % user.id
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'app_notification',
                "data": {
                    "event": str(event),
                    "sender_id": instance.user.id,
                    "sender_name":str(instance.user.profile.name),
                    "subject_data":"comment",
                    "subject_id":instance.id,
                    "object_data":"post",
                    "object_id": obj.id,
                },
            }
        )

post_save.connect(CommentNotification, sender=Comment, dispatch_uid="unique")

def ReplyNotification(sender,instance,created,**kwargs):
    channel_layer = get_channel_layer()
    user = instance.comment.user
    event = "replied_comment"
    obj = instance.comment
    if created and user.id is not instance.user.id:
        Notification.objects.create(
            user=user,
            event=str(event),
            sender_id=instance.user.id,
            subject_data = "reply",
            subject_id = instance.id,
            subject_text_preview = str(instance.text),
            object_data = "comment",
            object_id=obj.id,
            object_text_preview = str(obj.text),
        )
        group_name = "notification_%s" % user.id
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'app_notification',
                "data": {
                    "event": str(event),
                    "sender_id": instance.user.id,
                    "sender_name":str(instance.user.profile.name),
                    "subject_data":"reply",
                    "subject_id":instance.id,
                    "object_data":"comment",
                    "object_id": obj.id,
                },
            }
        )

post_save.connect(ReplyNotification, sender=Reply, dispatch_uid="unique")