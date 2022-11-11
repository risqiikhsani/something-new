from django.db.models.signals import post_save

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import *

from .helpers import get_random_alphanumeric_string

from django.conf import settings

from django.core.mail import send_mail

def createProfile(sender,instance,created,**kwargs):
    if created:
        random_unique_string = str(get_random_alphanumeric_string(5)) + str(instance.id) + str(get_random_alphanumeric_string(5))
        profile = Profile.objects.create(
            user=instance,
            public_username= random_unique_string,
            name= random_unique_string,
        )

        connection = Connection.objects.create(
            user=instance,
        )

        print("createProfile signal was called")

        #send email
        # app_name = "Testing"
        # name = "Bruh"
        # subject = f'Welcome to {app_name} App'
        # message = f'Hi {name} ,thankyou for registering in {app_name}.'
        # email_from = settings.EMAIL_HOST_USER
        # recepient_list = [instance.email,]
        # send_mail(subject,message,email_from,recepient_list)

                
post_save.connect(createProfile,sender=User,dispatch_uid="unique")