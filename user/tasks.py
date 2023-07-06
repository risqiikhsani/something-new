import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse

from something.celery import app


@app.task
def send_email(subject, message, recipient_list):
    email_from = settings.EMAIL_HOST_USER

    send_mail(
        subject=subject,
        message=message,
        from_email=email_from,
        recipient_list=recipient_list,
        fail_silently=False
    )
