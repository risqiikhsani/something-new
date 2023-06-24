from django_filters.rest_framework import DjangoFilterBackend
from http import server
from os import stat

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q
from django.core.exceptions import ValidationError

from rest_framework import generics, mixins, response, decorators, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
# Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


from .permissions import IsStaffOrReadOnly
from ..models import *
from django.conf import settings
# User = settings.AUTH_USER_MODEL

from django.contrib.auth import get_user_model
User = get_user_model()





from .serializers import User_Serializer
class UserList(mixins.ListModelMixin,
			   mixins.CreateModelMixin,generics.GenericAPIView):
	serializer_class = User_Serializer
	permission_classes = [permissions.IsAuthenticated,IsStaffOrReadOnly]
	queryset = User.objects.all()
	
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=201)
	

class UserDetail(generics.GenericAPIView):
	queryset = User.objects.all()
	serializer_class = User_Serializer
	permission_classes = [permissions.IsAuthenticated,IsStaffOrReadOnly]

	def get_object(self, id):
		try:
			return self.get_queryset().get(id=id)
		except User.DoesNotExist:
			return Response(status=404)

	def get(self, request, id):
		user = self.get_object(id)
		serializer = self.get_serializer(user)
		return Response(serializer.data,status=200)

	def put(self, request, id):
		user = self.get_object(id)
		serializer = self.get_serializer(user, data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data,status=201)

	def delete(self, request, id):
		user = self.get_object(id)
		user.delete()
		return Response(status=204)


	
	

