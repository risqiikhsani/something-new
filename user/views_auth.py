from http import server
from os import stat

# Token
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse
from rest_framework import (decorators, generics, mixins, permissions,
                            response, serializers, status)
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from versatileimagefield.serializers import VersatileImageFieldSerializer

from .models import *
from .permissions import IsOwnerOrReadOnly
from .serializers_auth import (ChangePassword_Serializer, Login_Serializer,
                               Register_Serializer, User_Simple_Serializer)

User = get_user_model()

from datetime import timedelta

from django.utils import timezone


class Register(generics.GenericAPIView):
	permission_classes = [permissions.AllowAny, ]
	serializer_class = Register_Serializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			return Response({"message":"Account registered successfully!"}, status.HTTP_201_CREATED)



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

# from .serializers_auth import ForgotPassword_Serializer
# class ForgotPassword(generics.GenericAPIView):
#     serializer_class = ForgotPassword_Serializer

#     def post(self,request,*args,**kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             email = serializer.validated_data['email']
#             user = get_object_or_404(User,email=email)
#             token = default_token_generator.make_token(user)
#             # save password reset request
#             password_reset_request = PasswordResetRequest(user=user, token=token)
#             password_reset_request.save()
#             # send email
#             app_name = "Testing"
#             name = user.profile.name
#             verification_url = token
#             subject = f'Verification from {app_name} App'
#             message = f'Hi {name} , Visit this link to reset your password. {verification_url} . The link will expire in 10 minutes.'
#             email_from = settings.EMAIL_HOST_USER
#             recepient_list = [user.email,]
#             send_mail(subject,message,email_from,recepient_list,fail_silently=False,)
#             return Response({"message":"Reset Password Guide has been sent to email"},status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# from .serializers_auth import ForgotPasswordConfirm_Serializer
# class ForgotPasswordConfirm(generics.GenericAPIView):
#     serializer_class = ForgotPasswordConfirm_Serializer

#     def put(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             token = serializer.validated_data['token']
#             new_password = serializer.validated_data['password']

#             try:
#                 password_reset_request = PasswordResetRequest.objects.get(token=token)
#                 user = password_reset_request.user
#                 expiration_time = password_reset_request.created_at + timedelta(minutes=10)
#                 if timezone.now() > expiration_time:
#                         return Response({'detail': 'Token has expired.'}, status=status.HTTP_400_BAD_REQUEST)

#                 # Reset the user's password
#                 user.set_password(new_password)
#                 user.save()
#             except PasswordResetRequest.DoesNotExist:
#                 return Response({'detail': 'Token has expired.'}, status=status.HTTP_400_BAD_REQUEST)
#             return Response({"message":"Password updated successfully"},status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from random import randint

from .serializers_auth import ForgotPassword_Serializer


class ForgotPassword(generics.GenericAPIView):
	serializer_class = ForgotPassword_Serializer

	def post(self,request,*args,**kwargs):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			email = serializer.validated_data['email']
			user = get_object_or_404(User,email=email)
			verification_code = str(randint(1000, 9999))
			# save password reset request
			password_reset_request = PasswordResetRequest(user=user, code=verification_code)
			password_reset_request.save()   # will trigger signal to send email
			return Response({"message":"Reset Password Guide has been sent to email"},status=status.HTTP_201_CREATED)

from .serializers_auth import ForgotPasswordCheck_Serializer


class ForgotPasswordCheckOptional(generics.GenericAPIView):
	serializer_class = ForgotPasswordCheck_Serializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			code = serializer.validated_data.get('code')
			email = serializer.validated_data.get('email')
			user = get_object_or_404(User, email=email)
			password_reset_request = get_object_or_404(PasswordResetRequest, code=code, user=user)
			expiration_time = password_reset_request.created_at + timedelta(minutes=10)
			if timezone.now() > expiration_time:
				return Response({'detail': 'Token has expired.'}, status=status.HTTP_400_BAD_REQUEST)
			return Response(status=status.HTTP_200_OK)


from .serializers_auth import ForgotPasswordConfirm_Serializer


class ForgotPasswordConfirm(generics.GenericAPIView):
	serializer_class = ForgotPasswordConfirm_Serializer

	def put(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			code = serializer.validated_data.get('code')
			email = serializer.validated_data.get('email')
			token = serializer.validated_data.get('token')
			new_password = serializer.validated_data['password']
			user = get_object_or_404(User, email=email)
			password_reset_request = get_object_or_404(PasswordResetRequest, code=code, user=user)
			expiration_time = password_reset_request.created_at + timedelta(minutes=10)
			if timezone.now() > expiration_time:
				return Response({'detail': 'Token has expired.'}, status=status.HTTP_400_BAD_REQUEST)

			# Reset the user's password
			user.set_password(new_password)
			user.save()
			return Response({"message": "Password updated successfully"}, status=status.HTTP_201_CREATED)


class ChangePassword(generics.GenericAPIView):
	serializer_class = ChangePassword_Serializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def get_queryset(self):
		return get_object_or_404(User, id=self.request.user.id)

	def put(self, request, *args, **kwargs):
		queryset = self.get_queryset()

		serializer = self.get_serializer(instance=queryset, context={'request': request}, data=request.data)
		if serializer.is_valid(raise_exception=True):
			return Response({"message": "password updated successfully"}, status=status.HTTP_201_CREATED)




class SendEmailVerification(generics.GenericAPIView):
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return get_object_or_404(User, id=self.request.user.id)

	# send uuid to email by signal
	def get(self, request, *args, **kwargs):
		verification = Verification.objects.create(user=self.request.user)
		verification.save()

		return Response({"message":"verification sent"}, status=status.HTTP_201_CREATED)


class EmailVerification(generics.GenericAPIView):
	permission_classes = [permissions.AllowAny]

	def get(self, request, *args, **kwargs):
		uuid = self.kwargs["uuid"]
		verification = get_object_or_404(Verification, uuid=uuid)
		if verification.user.email_verified == False:
			user = verification.user
			user.email_verified = True
			user.save()

		return Response({"message":"email has been verified successfully"}, status=status.HTTP_201_CREATED)
