from typing_extensions import Required
from django.db import models

import uuid
# Create your models here.
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from versatileimagefield.fields import VersatileImageField

# from django.contrib.auth import get_user_model
# User = get_user_model()

from django.conf import settings
User = settings.AUTH_USER_MODEL


from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
	    return str(self.id)


class Verification(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	code = models.CharField(max_length=50,null=True,blank=True)
	uuid = models.UUIDField(default=uuid.uuid4)
	time_creation = models.DateTimeField(auto_now_add=True,null=True,blank=True)

	def __str__(self):
		return str(self.id)


class CustomUser(AbstractUser):
	phone_number = PhoneNumberField(null=True,blank=True)
	email_verified = models.BooleanField(default=False,null=True,blank=True)
	first_name = None
	last_name = None
	
	def __str__(self):
		return self.username
	
	def get_connections_amount(self):
		return self.connection.connected.all().count()
	

from .helpers import get_random_alphanumeric_string
def get_upload_path(instance,filename):
	ext = filename.split('.')[-1]
	randomfilename = get_random_alphanumeric_string(20)
	resultfilename = "%s.%s" % (randomfilename, ext)
	return 'user/{}/profile/{}'.format(instance.user.id,resultfilename)

from django.core.exceptions import ValidationError

def file_size(value): # add this to some file where you can import it from
    limit = 8 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 8 MiB.')

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	public_username = models.CharField(max_length=100, null=True, blank=True,unique=True)

	about = models.TextField(blank=True,null=True)
	profile_picture = VersatileImageField(
		upload_to=get_upload_path,
		validators=[file_size],
		null=True,
		blank=True
	)

	poster_picture = VersatileImageField(
		upload_to=get_upload_path,
		validators=[file_size],
		null=True,
		blank=True
	)

	def __str__(self):
		return str(self.id)


class Connection(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	connected = models.ManyToManyField('self',blank=True)
	
	def __str__(self):
		return str(self.id)
	


class Block(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blocked_by")

	def __str__(self):
		return str(self.id)

class Relationship(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="relationship_by")
	pin = models.BooleanField(default=False)
	follow = models.BooleanField(default=True)
	notification = models.BooleanField(default=False)
	nickname = models.CharField(max_length=100,null=True,blank=True)
	time_creation = models.DateTimeField(auto_now_add=True,null=True,blank=True)

	def __str__(self):
		return str(self.id)


class Request(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	sender = models.ForeignKey(User,related_name="request_to", on_delete=models.CASCADE)
	time_creation = models.DateTimeField(auto_now_add=True,null=True)
	accept = models.BooleanField(default=False,null=True,blank=True)
	decline = models.BooleanField(default=False,null=True,blank=True)

	def __str__(self):
		return str(self.id)


# class Account(models.Model):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


# 	def __str__(self):
# 		return str(self.id)