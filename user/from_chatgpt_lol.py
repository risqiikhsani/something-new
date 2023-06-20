# serializers.py
from rest_framework import serializers

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

# views.py
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ForgotPasswordSerializer
from django.contrib.auth.tokens import default_token_generator

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            reset_link = f"{current_site.domain}/api/password/reset/confirm/{uid}/{token}/"

            mail_subject = 'Reset your password'
            message = render_to_string('reset_password_email.html', {
                'reset_link': reset_link,
            })
            send_mail(mail_subject, message, 'noreply@example.com', [email])
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#############################################################################

# serializers.py
from django.contrib.auth.forms import SetPasswordForm
from rest_framework import serializers

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    def validate(self, attrs):
        password = attrs['password']
        password_confirm = attrs['password_confirm']
        uid = self.context['uid']
        token = self.context['token']

        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Invalid or expired token.')

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError('Invalid or expired token.')

        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match.')

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        password = self.validated_data['password']
        user.set_password(password)
        user.save()

# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ResetPasswordSerializer

class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer(data=request.data,
