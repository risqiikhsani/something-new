

from .serializers import User_Serializer, User_Simple_Serializer
from .serializers import Request_Serializer
from .serializers import Connection_Serializer
from .serializers import my_user_serializer,my_profile_serializer
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


from .permissions import IsOwnerOrReadOnly
from .models import *
from django.conf import settings
# User = settings.AUTH_USER_MODEL

from django.contrib.auth import get_user_model
User = get_user_model()

from something.pagination import MycustomPagination

@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),

	})

# Using mixins
# https://www.django-rest-framework.org/tutorial/3-class-based-views/


class UserList(mixins.ListModelMixin, generics.GenericAPIView):
	serializer_class = User_Simple_Serializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset = User.objects.all()

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)


class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = User_Serializer
	
class my_user(generics.RetrieveUpdateAPIView):
	parser_classes = (JSONParser, MultiPartParser, FormParser)
	serializer_class = my_user_serializer
	queryset = User.objects.all()

	# note = set get_object to exclude lookup_url when calling RetrieveAPIView
	def get_object(self):
		queryset = self.get_queryset()
		obj = get_object_or_404(queryset, id=self.request.user.id)
		return obj
	
	
class my_profile(generics.RetrieveUpdateAPIView):
	parser_classes = (JSONParser, MultiPartParser, FormParser)
	serializer_class = my_profile_serializer
	queryset = Profile.objects.all()
	
	# note = set get_object to exclude lookup_url when calling RetrieveAPIView
	def get_object(self):
		queryset = self.get_queryset()
		obj = get_object_or_404(queryset, user=self.request.user)
		return obj


 
class ConnectionViewSet(viewsets.ReadOnlyModelViewSet):
# https://stackoverflow.com/questions/31785966/django-rest-framework-turn-on-pagination-on-a-viewset-like-modelviewset-pagina
# class ConnectionViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
	serializer_class = Connection_Serializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
	queryset = Connection.objects.all()

	def list(self,request):
		queryset = self.get_queryset()
		connection = get_object_or_404(queryset, user=self.request.user)
		connections = connection.connected.all()
		serializer = self.get_serializer(connections, many=True)
		return Response(serializer.data)


	
	@action(detail=True)
	def remove_connection(self,request,pk=None):
		queryset = self.get_queryset()
		connection = get_object_or_404(queryset, pk=pk)
		my_connection = self.request.user.connection
		my_connection.connected.remove(connection)
		return Response("connection is successfully removed",status=status.HTTP_200_OK)

		
class RequestViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = Request_Serializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

	def get_queryset(self):
		return Request.objects.all().order_by('-time_creation')

	def list(self,request):
		queryset = self.get_queryset()
		my_request_list = get_list_or_404(queryset, user=self.request.user)
		serializer = self.get_serializer(my_request_list, many=True)
		return Response(serializer.data)


	@action(detail=True)
	def accept_request(self,request,pk=None):
		queryset = self.get_queryset()
		obj = get_object_or_404(queryset, pk=pk)
		if obj.user == self.request.user:
			obj.accept = True
			obj.save()
			return Response("sucessfully accept request",status=status.HTTP_200_OK)
		return Response("UNAUTHORIZED",status=status.HTTP_401_UNAUTHORIZED)

	@action(detail=True)
	def decline_request(self,request,pk=None):
		queryset = self.get_queryset()
		obj = get_object_or_404(queryset, pk=pk)
		if obj.user == self.request.user:
			obj.decline = True
			obj.save()
			return Response("sucessfully decline request",status=status.HTTP_200_OK)
		return Response("UNAUTHORIZED",status=status.HTTP_401_UNAUTHORIZED)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def get_queryset(self):
		return User.objects.all()

	@action(detail=True)
	def send_request(self,request,pk=None):
		user = get_object_or_404(User, pk=pk)
		obj, created = Request.objects.get_or_create(user=user, sender=self.request.user )
		if created == False:
			return Response("failed , request already exists",status=status.HTTP_404_NOT_FOUND)
		return Response("request has been sent",status=status.HTTP_201_CREATED)

	@action(detail=True)
	def cancel_sent_request(self,request,pk=None):
		user = get_object_or_404(User, pk=pk)
		obj = Request.objects.get(user=user, sender=self.request.user)
		if not obj:
			return Response("failed, request isn't exists",status=status.HTTP_404_NOT_FOUND)
		obj.delete()
		return Response("successfully cancel the request",status=status.HTTP_200_OK)

	def user_connection_list(self,request,pk=None):
		user = get_object_or_404(User, pk=pk)
		obj = user.connection.connected.all()
		print(obj)
		serializer = Connection_Serializer(obj,many=True)
		return Response(serializer.data)
	


# class ConnectionList(mixins.ListModelMixin, generics.GenericAPIView):
# 	serializer_class = Connection_Serializer
# 	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 	def get_queryset(self):
# 		connection = Connection.objects.get(user=self.request.user)
# 		return connection.connected.all()

# 	def get(self, request, *args, **kwargs):
# 		return self.list(request, *args, **kwargs)


# class ConnetionDetail(generics.GenericAPIView):
# 	serializer_class = Connection_Serializer
# 	permission_classes = [
# 	    permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# 	def get_queryset(self):
# 		return get_object_or_404(Connection, user=self.request.user)

# 	def get(self, request, *args, **kwargs):
# 		queryset = self.get_queryset()
# 		connected = get_object_or_404(
# 		    queryset.connected.all(), id=self.kwargs['connection_id'])
# 		serializer = self.get_serializer(instance=connected)
# 		return Response(serializer.data)

# 	def delete(self, request, *args, **kwargs):
# 		queryset = self.get_queryset()
# 		connected = get_object_or_404(
# 		    queryset.connected.all(), id=self.kwargs['connection_id'])
# 		queryset.remove(connected)
# 		return Response("deleted", status=status.HTTP_204_NO_CONTENT)


# class RequestList(mixins.ListModelMixin, generics.GenericAPIView):
# 	serializer_class = Request_Serializer
# 	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# 	def get_queryset(self):
# 		return Request.objects.all().filter(user=self.request.user)

# 	def get(self, request, *args, **kwargs):
# 		return self.list(request, *args, **kwargs)


# class RequestDetail(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
# 	serializer_class = Request_Serializer
# 	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
# 	queryset = Request.objects.all()



# 	def get(self, request, *args, **kwargs):
# 		return self.retrieve(request, *args, **kwargs)
	
# 	def delete(self, request, *args, **kwargs):
# 		return self.destroy(request, *args, **kwargs)
