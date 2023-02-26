from django.db import models



# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()
from versatileimagefield.fields import VersatileImageField


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