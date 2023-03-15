import logging

from django.urls import reverse

from django.core.mail import send_mail

from django.contrib.auth import get_user_model

from something.celery import app

from django.conf import settings

@app.task

def send_welcome_email(instance):
    app_name = "Testing"
    name = instance.username
    subject = f'Welcome to {app_name} App'
    message = f'Hi {name} ,thankyou for registering in {app_name}.'
    email_from = settings.EMAIL_HOST_USER
    recepient_list = [instance.email,]
    send_mail(subject,message,email_from,recepient_list,fail_silently=False,)
