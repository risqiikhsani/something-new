from django_filters.rest_framework import DjangoFilterBackend
from http import server
from os import stat

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q, Max

from django.core.exceptions import ValidationError

from rest_framework import generics, mixins, response, decorators, permissions, status, viewsets, filters
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.decorators import action
# Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()



from .serializers import Notification_Serializer
class NotificationList(generics.ListAPIView):
    serializer_class = Notification_Serializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notification_set.all().order_by('-time_creation')
    

from .serializers import ChatRoom_Serializer
class ChatRoomList(generics.ListAPIView):
    serializer_class = ChatRoom_Serializer
    permission_classes = [permissions.IsAuthenticated]
    

    def get_queryset(self):
        # https://docs.djangoproject.com/en/4.1/topics/db/aggregation/
        return ChatRoom.objects.all().filter(user=self.request.user).annotate(last_chat_date=Max('chat__time_creation')).order_by('last_chat_date')    
    

class GetOrCreateChatRoom(generics.GenericAPIView):

    serializer_class = ChatRoom_Serializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_object_or_404(User, id=self.kwargs["user_id"])
    
    def get(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        try:
            a = ChatRoom.objects.get(
                Q(type="twoperson"),
                Q(user=self.request.user),
                Q(user=queryset)
            )
        except ChatRoom.DoesNotExist:
            a = ChatRoom.objects.create(type="twoperson")
            a.user.add(self.request.user,queryset)
            a.save()
        print(a.id)
        data = {
            "chatroom_id":str(a.id),
        }
        return Response(data,status=status.HTTP_201_CREATED)


    

# class NotificationList(mixins.ListModelMixin, generics.GenericAPIView):
#     serializer_class = Notification_Serializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return self.request.user.notification_set.all().order_by('-time_creation')

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
