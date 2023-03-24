from .serializers_auth import Login_Serializer
from .serializers_auth import ChangePassword_Serializer
from versatileimagefield.serializers import VersatileImageFieldSerializer
from .serializers_auth import User_Simple_Serializer
from .serializers_auth import Register_Serializer
from http import server
from os import stat
from urllib.parse import urlencode

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
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

from .services import google_get_access_token
from .services import google_get_user_info

# redirect this url from google credential redirect uri

# class GoogleLoginApi(generics.GenericAPIView):
#     #class InputSerializer(serializers.Serializer):
#         # code = serializers.CharField(required=False)
#         # error = serializers.CharField(required=False)

#     def get(self, request, *args, **kwargs):
#         # input_serializer = self.InputSerializer(data=request.GET)
#         # input_serializer.is_valid(raise_exception=True)

#         # validated_data = input_serializer.validated_data

#         # code = validated_data.get('code')
#         # error = validated_data.get('error')

#         # if error or not code:
#         #     login_url = f'{settings.BASE_FRONTEND_URL}/login'
#         #     params = urlencode({'error': error})
#         #     return redirect(f'{login_url}?{params}')

#         code = self.request.query_params.get('code')
#         print(code)


#         domain = settings.BASE_BACKEND_URL
#         api_uri = reverse('login-google')
#         redirect_uri = f'{domain}{api_uri}'

#         access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

#         print("access_token :" + access_token)

#         user_data = google_get_user_info(access_token=access_token)

#         print(user_data)

#         response = redirect(f'{settings.BASE_FRONTEND_LOGIN_URL}')

#         # profile_data = {
#         #     'email': user_data['email'],
#         #     'first_name': user_data.get('given_name', ''),
#         #     'last_name': user_data.get('family_name', ''),
#         # }

#         # # We use get-or-create logic here for the sake of the example.
#         # # We don't have a sign-up flow.
#         # user, _ = User.objects.get_or_create(email=user_data['email'])

        
#         # login_url = f'{settings.BASE_FRONTEND_LOGIN_URL}'
#         # params = urlencode({
#         #     'access_token': accessToken,
#         #     'refresh_token':refreshToken,
#         #     })
#         # response = redirect(f'{login_url}?{params}')

#         return response




# exchange code in backend with post

class Code_Serializer(serializers.Serializer):
    code = serializers.CharField(required=False)

class GoogleLoginApi(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = Code_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            code = serializer.validated_data['code']
            print(code)
            redirect_uri = f'{settings.BASE_FRONTEND_LOGIN_URL}'
            access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
            print("access_token :" + access_token)
            user_data = google_get_user_info(access_token=access_token)
            print(user_data)
            email = user_data['email']
            user,_ = User.objects.get_or_create(email=email)
            user.save()

            refresh = self.get_tokens_for_user(user)

            data = {
                'user': User_Simple_Serializer(instance=user, context={'request': request}).data,
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)