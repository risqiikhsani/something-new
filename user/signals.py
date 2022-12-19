from django.db.models.signals import post_save,m2m_changed,post_delete

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import *

from .helpers import get_random_alphanumeric_string

from django.conf import settings

from django.core.mail import send_mail

def userMainSignal(sender,instance,created,**kwargs):
    if created:
        print("signal : create profile")
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

        

        #send email
        # app_name = "Testing"
        # name = "Bruh"
        # subject = f'Welcome to {app_name} App'
        # message = f'Hi {name} ,thankyou for registering in {app_name}.'
        # email_from = settings.EMAIL_HOST_USER
        # recepient_list = [instance.email,]
        # send_mail(subject,message,email_from,recepient_list)


                
post_save.connect(userMainSignal,sender=User,dispatch_uid="unique")

def requestAction(sender,instance,created,**kwargs):
    # if user accept the friend request , user will be friend/connected with the request sender
    if instance.accept == True:
        print("signal : connection handler")
        instance.user.connection.connected.add(instance.sender.connection)

    # if user decline the friend request , request will be deleted
    if instance.decline == True:
        print("signal : connection handler")
        instance.delete()


post_save.connect(requestAction,sender=Request,dispatch_uid="unique")


# https://docs.djangoproject.com/en/4.1/ref/signals/#m2m-changed
def connectionM2mAction(sender,instance,action,pk_set,model,**kwargs):
    # if user connected with other user , do this
    if action == 'post_add':
        print(sender)
        print(instance)
        print(action)
        print(pk_set)
        print(model)
        # <class 'user.models.Connection_connected'>
        # 2
        # post_add
        # {1}
        # <class 'user.models.Connection'>

        # create 2 relationship for each
        user = instance.user
        to_user = model.objects.get(pk=list(pk_set)[0]).user

        r1,created = Relationship.get_or_create(user = user,to_user = to_user,)
        r1.save()

        r2, created = Relationship.get_or_create(user= to_user,to_user = user,)
        r2.save()

    # if user disconnected from other user, do this
    elif action == 'post_remove':
        # delete 2 relationship for each
        user = instance.user
        to_user = model.objects.get(pk=list(pk_set)[0]).user
        r1 = Relationship.objects.get(user=user,to_user=to_user)
        r2 = Relationship.objects.get(user=to_user,to_user=user)
        r1.delete()
        r2.delete()

m2m_changed.connect(connectionM2mAction,sender=Connection.connected.through)

# when the user block others
def blockCreatedAction(sender,instance,created,**kwargs):
    # if the block is created
    if created:
        # if connection of them was exist
        if instance.user.connection.connected.filter(user=instance.blocked).exists():
            # remove the connection
            c1 = Connection.objects.get(user=instance.user)
            c2 = Connection.objects.get(user= instance.blocked)
            c1.connected.remove(c2)

post_save.connect(blockCreatedAction,sender=Block,dispatch_uid="unique")


# when the user unblock others
def blockDeletedAction(sender,instance,*args,**kwargs):
    # if request of accepted was exists . means they were friends
    if Request.objects.filter(user=instance.user,sender=instance.blocked,accept=True).exists():
        # recreate the connection
        instance.user.connection.connected.add(instance.blocked.connection)

post_delete.connect(blockDeletedAction,sender=Block,dispatch_uid="unique")

