


from http import server
from os import stat

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q
from django.core.exceptions import ValidationError

from rest_framework import generics, mixins,response, decorators, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
# Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


from .permissions import IsOwnerOrReadOnly
from .models import *
from django.conf import settings
# User = settings.AUTH_USER_MODEL

from django.contrib.auth import get_user_model
User = get_user_model()


from django_filters.rest_framework import DjangoFilterBackend

@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		
	})

# Using mixins
# https://www.django-rest-framework.org/tutorial/3-class-based-views/

from .serializers import User_Serializer
class UserList(mixins.ListModelMixin,generics.GenericAPIView):
	serializer_class = User_Serializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset = User.objects.all()

	def get(self, request, *args, **kwargs):
		return self.list(request,*args,**kwargs)

from .serializers import User_Serializer
class UserDetail(mixins.RetrieveModelMixin,
					mixins.UpdateModelMixin,
					mixins.DestroyModelMixin,
					generics.GenericAPIView):
	queryset = User.objects.all()				
	serializer_class = User_Serializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)
