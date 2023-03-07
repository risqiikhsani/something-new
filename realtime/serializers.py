import json
from queue import Empty

from rest_framework import serializers

from .models import *


from versatileimagefield.serializers import VersatileImageFieldSerializer

from user.serializers import User_Simple_Serializer

from django.contrib.auth import get_user_model
User = get_user_model()




class Notification_Serializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    natural_time = serializers.CharField(source="get_natural_time",required=False)
    class Meta:
        model = Notification
        fields = ['id','event','sender','subject_data','subject_id','object_data','object_id','natural_time']

    def get_sender(self,obj):
        sender = User.objects.get(id=obj.sender_id)
        return User_Simple_Serializer(instance=sender,context={'request':self.context['request']}).data



class Chat_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class ChatRoom_Serializer(serializers.ModelSerializer):
    last_chat = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()
    # websocket_group_name = serializers.SerializerMethodField()
    class Meta:
        model = ChatRoom
        fields = ['id','type','time_creation','last_chat','display']
        order_by = ['']

    
    def get_last_chat(self,obj):
        try:
            a = obj.chat_set.all().latest('id')
            return Chat_Serializer(instance=a,context={'request':self.context['request']}).data
        except Chat.DoesNotExist:
            return None    
        
    def get_display(self,obj):
        if obj.type == "group":
            return None
        else:
            user = obj.user.all().exclude(id=self.context['request'].user.id).latest('id')
            return User_Simple_Serializer(instance=user,context={'request':self.context['request']}).data
        
    # def get_websocket_group_name(self,obj):
    #     return "chatroom_%s" % obj.id
        