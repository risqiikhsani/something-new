from django_filters.rest_framework import DjangoFilterBackend
from http import server
from os import stat

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q

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
        return self.request.user.connection_set.all().order_by('-time_creation')

