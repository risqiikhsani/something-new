from django.db.models.signals import post_save,m2m_changed

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

def requestMainSignal(sender,instance,created,**kwargs):
    # if user accept the friend request , user will be friend/connected with the request sender
    if instance.accept == True:
        print("signal : connection handler")
        instance.user.connection.connected.add(instance.sender.connection)

    # if user decline the friend request , request will be deleted
    if instance.decline == True:
        print("signal : connection handler")
        instance.delete()


post_save.connect(requestMainSignal,sender=Request,dispatch_uid="unique")

# https://docs.djangoproject.com/en/4.1/ref/signals/#m2m-changed
def connectionMainSignal(sender,instance,action,pk_set,model,**kwargs):
    if action == 'post_add':
        # create relationship
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
        user = instance.user
        to_user = model.objects.get(pk=list(pk_set)[0]).user

        # create 2 relationships for each?
        obj = Relationship.create(
            user = user,
            to_user = to_user,
        )
        obj.save()

        obj2 = Relationship.create(
            user= to_user,
            to_user = user,
        )

        obj2.save()
    elif action == 'post_remove':
        pass

m2m_changed.connect(connectionMainSignal,sender=Connection.connected.through)

def relationshipMainSignal(sender,instance,created,**kwargs):
    if instance.block == True:
        c = Connection.object.get(user=instance.user)
        obj = Connection.object.get(user=instance.to_user)
        c.connected.remove(obj)

    if instance.block == False:
        c = Connection.object.get(user=instance.user)
        obj = Connection.object.get(user=instance.to_user)
        c.connected.add(obj)

post_save.connect(relationshipMainSignal,sender=Relationship,dispatch_uid="unique")
