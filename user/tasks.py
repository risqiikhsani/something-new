import logging

from django.urls import reverse

from django.core.mail import send_mail

from django.contrib.auth import get_user_model

from something.celery import app

from django.conf import settings



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
