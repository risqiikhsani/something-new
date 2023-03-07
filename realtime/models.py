from django.db import models



# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()
from versatileimagefield.fields import VersatileImageField
from django.contrib.humanize.templatetags import humanize

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    event = models.CharField(max_length=100,null=True,blank=True)
    sender_id = models.IntegerField(null=True,blank=True)
    subject_data = models.CharField(null=True,blank=True,max_length=100)
    subject_id = models.IntegerField(null=True,blank=True)
    subject_text_preview = models.TextField(null=True,blank=True)
    object_data = models.CharField(null=True,blank=True,max_length=100)
    object_id = models.IntegerField(null=True,blank=True)
    object_text_preview = models.TextField(null=True,blank=True)
    time_creation = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return str(self.id)
    
    def get_natural_time(self):
        return humanize.naturaltime(self.time_creation)

    def get_natural_day(self):
        return humanize.naturalday(self.time_creation)


class Client(models.Model):
    SERVER_CHOICES = [
        ("app_notification","app_notification"),
        ("chat_notification","chat_notification"),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    channel_name = models.CharField(max_length=100,null=True,blank=True)
    server = models.CharField(choices=SERVER_CHOICES,max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.id)
    
class ClientSocketData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    last_read_id_in_server = models.IntegerField(default=0)
    server_name = models.CharField(null=True,blank=True,max_length=300)
    # unread_item_in_server = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.id)
    
class ChatRoom(models.Model):
    TYPE_CHOICES = [
        ("twoperson","twoperson"),
        ("group","group"),
    ]
    type = models.CharField(max_length=100,choices=TYPE_CHOICES)
    user = models.ManyToManyField(User,blank=True)
    time_creation = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_last_chat_date(self):
        try:
            return self.chat_set.all().latest('id').time_creation
        except Chat.DoesNotExist:
            return self.time_creation


    
class GroupChatRoom(models.Model):
    time_creation = models.DateTimeField(auto_now_add=True,null=True)
    generated_link = models.CharField(null=True,blank=True,max_length=100)

    def __str__(self):
        return str(self.id)


class Chat(models.Model):
    room = models.ManyToManyField(ChatRoom,blank=True)
    sender = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    text = models.TextField(null=True,blank=True)
    time_creation = models.DateTimeField(auto_now_add=True,null=True)
    time_update = models.DateTimeField(auto_now=True,null=True,blank=True)
    forwarded = models.BooleanField(null=True,blank=True,default=False)
    reply_from = models.ForeignKey('self',on_delete=models.DO_NOTHING, null=True,blank=True)

    def __str__(self):
        return str(self.id)
    
    def get_natural_time(self):
        return humanize.naturaltime(self.time_creation)

    
