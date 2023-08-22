import os

from django.contrib.auth import get_user_model
from django.db.models.signals import (m2m_changed, post_delete, post_save,
                                      pre_save)

User = get_user_model()

import logging

from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver

from .helpers import get_random_alphanumeric_string
from .models import *
from .tasks import *

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Verification, dispatch_uid="unique")
def verificationSignal(sender,instance,created,**kwargs):
    if created:
        # this is usually for changing email , require code verification sent to old email
        if instance.code:
            if instance.user.email:
                pass
        # this is for email verification account
        if instance.uuid:
            if not instance.user.email_verified:
                if instance.user.email:
                    recipient_list = [instance.email,]
                    app_name = "Testing"
                    subject = f'Verification from{app_name} App'
                    verification_url = instance.uuid
                    user = instance.user.profile.name
                    text = f'Visit this link to verify your email address. {verification_url}'
                    send_email.delay(subject,user,text,recipient_list)
                    logger.info('[Email verification email] is sent to user_id={}'.format(instance.user.id))
                    


@receiver(post_save,sender=PasswordResetRequest,dispatch_uid="unique")
def ForgotPasswordSignal(sender,instance,created,**kwargs):
    if created:
        app_name = "Testing"
        subject = f'Verification from {app_name} App'
        recipient_list = [instance.user.email,]
        user=instance.user.profile.name
        text=f'This is your 4 digit verification code. {instance.code} . The code will expire in 10 minutes.'
        send_email.delay(subject,user,text,recipient_list)
        logger.info('[password reset request verification email] is sent to user_id={}'.format(instance.user.id))
        



@receiver(post_save, sender=User, dispatch_uid="unique")
def userMainSignal(sender,instance,created,**kwargs):
    # if user is created
    if created:
        logger.info("User Created. id = {}.".format(instance.id))
        random_unique_string = str(get_random_alphanumeric_string(5)) + str(instance.id) + str(get_random_alphanumeric_string(5))
        # create profile
        profile = Profile.objects.create(
            user=instance,
            public_username= random_unique_string,
            name= random_unique_string,
        )

        # create connection
        connection = Connection.objects.create(
            user=instance,
        )

        # if there's email, send a welcome email
        if instance.email:
            recipient_list = [instance.email,]
            app_name = "Testing"
            subject = f'Welcome to {app_name} App'
            user=instance.profile.name
            text=f'Welcome {instance.profile.name} ,thank you for registering in {app_name}.'
            send_email.delay(subject,user,text,recipient_list)
            logger.info('[Welcome to app email] is sent to user_id={}'.format(instance.id))
            
    # if user updated their account, send a notification email
    #if not created:
    else:
        if instance.email:
            recipient_list = [instance.email,]
            app_name = "Testing"
            subject = f'{app_name} App'
            user = instance.profile.name
            text = f'You have successfully updated your account in {app_name}.'
            send_email.delay(subject,user,text,recipient_list)
            logger.info('[user updated notification email] is sent to user_id={}'.format(instance.id))

        # Password has been updated, error !
        # if 'password' in instance.changed_fields:
        #     recipient_list = [instance.email,]
        #     app_name = "Testing"
        #     subject = f'{app_name} App'
        #     reset_password_url = 'http/localhost:3000/reset-password'
        #     message = f'Hi {instance.profile.name} , You have successfully changed your password. If it was not you , please reset your password. Visit this link {reset_password_url}'
        #     send_email.delay(subject,message,recipient_list)


@receiver(post_save, sender=Request, dispatch_uid="unique")
def requestAction(sender,instance,created,**kwargs):
    # TESTED = WORKS !
    # if user accept the friend request , user will be friend/connected with the request sender.
    # then the request will be deleted
    if instance.accept == True:
        instance.user.connection.connected.add(instance.sender.connection)
        instance.delete()

    # TESTED = WORKS !
    # if user decline the friend request , request will be deleted
    if instance.decline == True:
        instance.delete()



# https://docs.djangoproject.com/en/4.1/ref/signals/#m2m-changed
@receiver(m2m_changed, sender=Connection.connected.through)
def connectionM2mAction(sender, instance, action, pk_set, model, **kwargs):
     # if user connected with other user , do this
    if action == 'post_add':
        user = instance.user
        to_user = model.objects.get(pk=list(pk_set)[0]).user
        create_relationship(user, to_user)
        create_relationship(to_user, user)
     # if user disconnected from other user, do this
    elif action == 'post_remove':
        user = instance.user
        to_user = model.objects.get(pk=list(pk_set)[0]).user
        delete_relationship(user, to_user)
        delete_relationship(to_user, user)


def create_relationship(user, to_user):
    relationship, created = Relationship.objects.get_or_create(user=user, to_user=to_user)
    relationship.save()


def delete_relationship(user, to_user):
    try:
        relationship = Relationship.objects.get(user=user, to_user=to_user)
        relationship.delete()
    except Relationship.DoesNotExist:
        pass


# when the user block others
@receiver(post_save, sender=Block, dispatch_uid="unique")
def blockCreatedAction(sender,instance,created,**kwargs):
    # if the block is created
    if created:
        # if connection of them was exist
        if instance.user.connection.connected.filter(user=instance.blocked).exists():
            # remove the connection
            c1 = Connection.objects.get(user=instance.user)
            c2 = Connection.objects.get(user= instance.blocked)
            c1.connected.remove(c2)


# when the user unblock others
@receiver(post_delete, sender=Block, dispatch_uid="unique")
def blockDeletedAction(sender,instance,*args,**kwargs):
    # if request of accepted was exists . means they were friends
    if Request.objects.filter(user=instance.user,sender=instance.blocked,accept=True).exists():
        # recreate the connection
        instance.user.connection.connected.add(instance.blocked.connection)



@receiver(post_delete, sender=Profile, dispatch_uid="unique")
def auto_clear_files_on_delete(sender,instance,*args,**kwargs):
    # delete filtered and sized cache images
    instance.profile_picture.delete_all_created_images()
    instance.poster_picture.delete_all_created_images()
    try:
        # delete original image
        instance.profile_picture.delete(save=False)
    except:
        pass

    try:
        # delete original image
        instance.poster_picture.delete(save=False)
    except:
        pass



@receiver(pre_save, sender=Profile, dispatch_uid="unique")
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes the old file from the filesystem when corresponding `MediaFile` object is updated with a new file.
    """
    if not instance.pk:
        return False

    # Handle update/delete profile_picture
    handle_file_change(sender, instance, 'profile_picture')

    # Handle update/delete poster_picture
    handle_file_change(sender, instance, 'poster_picture')


def handle_file_change(sender, instance, field_name):
    old_file = get_old_file(sender, instance, field_name)
    new_file = get_new_file(sender, instance, field_name)

    if not old_file == new_file:
        if old_file and os.path.isfile(old_file.path):
            os.remove(old_file.path)
            old_file.delete_all_created_images()


def get_old_file(sender, instance, field_name):
    try:
        old_instance = sender.objects.get(pk=instance.pk)
        return getattr(old_instance, field_name)
    except sender.DoesNotExist:
        return None


def get_new_file(sender, instance, field_name):
    return getattr(instance, field_name)

# def auto_delete_file_on_change(sender,instance,**kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `MediaFile` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False

#     # handle update/delete profile_picture
#     try:
#         old_file = sender.objects.get(pk=instance.pk).profile_picture
#     except sender.DoesNotExist:
#         return False

#     new_file = instance.profile_picture
#     if not old_file == new_file:
#         if not old_file:
#             return False
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)
#             old_file.delete_all_created_images()
#     # handle update/delete poster_picture
#     try:
#         old_file_b = sender.objects.get(pk=instance.pk).poster_picture
#     except sender.DoesNotExist:
#         return False

#     new_file_b = instance.poster_picture
#     if not old_file_b == new_file_b:
#         if not old_file_b:
#             return False
#         if os.path.isfile(old_file_b.path):
#             os.remove(old_file_b.path)
#             old_file_b.delete_all_created_images()


# pre_save.connect(auto_delete_file_on_change,sender=Profile,dispatch_uid="unique")
