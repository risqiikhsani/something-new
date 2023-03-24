from .serializers_auth import Login_Serializer
from .serializers_auth import ChangePassword_Serializer
from versatileimagefield.serializers import VersatileImageFieldSerializer
from .serializers_auth import User_Simple_Serializer
from .serializers_auth import Register_Serializer
from http import server
from os import stat

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q
from django.urls import reverse
from django.core.exceptions import ValidationError

from rest_framework import generics, mixins, response, decorators, permissions, status
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser


# Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


from .permissions import IsOwnerOrReadOnly
from .models import *


from django.contrib.auth import get_user_model
User = get_user_model()



class Register(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = Register_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response("Account registered successfully!", status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = Login_Serializer

    def get_tokens_for_user(self, user):
        return RefreshToken.for_user(user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if not user:
                return Response({'error': 'invalid credentials'}, status=status.HTTP_404_NOT_FOUND)

            refresh = self.get_tokens_for_user(user)

            data = {
                'user': User_Simple_Serializer(instance=user, context={'request': request}).data,
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(generics.GenericAPIView):
    serializer_class = ChangePassword_Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return get_object_or_404(User, id=self.request.user.id)

    def put(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(instance=queryset, context={
                                         'request': request}, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("updated", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendEmailVerification(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_object_or_404(User, id=self.request.user.id)

    # send uuid to email by signal
    def get(self, request, *args, **kwargs):
        verification = Verification.objects.create(user=self.request.user)
        verification.save()

        return Response("verification sent", status=status.HTTP_201_CREATED)


class EmailVerification(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        uuid = self.kwargs["uuid"]
        verification = get_object_or_404(Verification, uuid=uuid)
        if verification.user.email_verified == False:
            user = verification.user
            user.email_verified = True
            user.save()

        return Response("email has been verified successfully", status=status.HTTP_201_CREATED)
