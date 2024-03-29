from http import server
from os import stat
from urllib.parse import urlencode

# Token
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)
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

from .services import google_get_access_token, google_get_user_info
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer

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
    permission_classes = ()
    serializer_class = Code_Serializer
    @extend_schema(
		request=Login_Serializer,
		responses={
			201: inline_serializer(
				name="Login Response",
				fields={
					"user": User_Simple_Serializer(),
					"refresh_token": serializers.CharField(),
					"access_token": serializers.CharField(),
				},
			),
			400: OpenApiResponse(description="Bad request (something invalid)"),
			404: OpenApiResponse(description="invalid credentials"),
		},
		description="Login user with google",
	)

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
