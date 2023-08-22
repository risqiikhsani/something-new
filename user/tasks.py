import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail,EmailMessage
from django.urls import reverse
from django.template.loader import render_to_string
from something.celery import app


@app.task
def send_email(subject, user,text, recipient_list):
    sender_email = settings.EMAIL_HOST_USER
    html_template = 'email.html'
    mydict = {
        'user':user,
        'text':text
    }
    html_message = render_to_string(html_template,context=mydict)
    message = EmailMessage(subject=subject,body=html_message,from_email=sender_email,to=recipient_list)
    message.content_subtype = 'html'
    message.send(fail_silently=False)

    # send_mail(
    #     subject=subject,
    #     message=html_message,
    #     from_email=email_from,
    #     recipient_list=recipient_list,
    #     fail_silently=False
    # )
