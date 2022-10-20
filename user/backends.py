from django.contrib.auth.backends import ModelBackend

from django.db.models import Q


from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

from django.contrib.auth import get_user_model
CustomUser = get_user_model()

# from django.conf import settings
# CustomUser = settings.AUTH_USER_MODEL






class AuthBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password) is True:
                return user
        except user.DoesNotExist:
            pass
