from ast import Or
from asyncio.windows_events import NULL
from django.contrib.auth.backends import ModelBackend

from django.db.models import Q


from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

# from django.conf import settings
# CustomUser = settings.AUTH_USER_MODEL






class AuthBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        print("custom backend is running")
        username = kwargs['username']
        password = kwargs['password']
        try:
            print("check username is running")
            # user = CustomUser.objects.get(username=username)
            user = CustomUser.objects.get(
                Q(username__exact=username) | 
                Q(email__exact=username) |
                Q(phone_number__exact=username)
            )
            if user.check_password(password) is True:
                return user
        except CustomUser.DoesNotExist:
            pass
