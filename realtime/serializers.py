import json
from queue import Empty
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


from versatileimagefield.serializers import VersatileImageFieldSerializer

from user.serializers import User_Serializer



class Notification_Serializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    natural_time = serializers.CharField(source="get_natural_time",required=False)
    class Meta:
        model = Notification
        fields = ['id','event','sender','subject_data','subject_id','object_data','object_id','natural_time']

    def get_sender(self,obj):
        sender = User.objects.get(id=obj.sender_id)
        return User_Serializer(instance=sender).data
