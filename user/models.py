from typing_extensions import Required
from django.db import models

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




class CustomUser(AbstractUser):
	phone_number = PhoneNumberField(null=True,blank=True)
	first_name = None
	last_name = None
	
	def __str__(self):
		return self.username
	



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	public_username = models.CharField(max_length=100, null=True, blank=True)

	about = models.TextField(blank=True,null=True)

	profile_picture = VersatileImageField(
		upload_to='images/profile_picture/',
		null=True,
		blank=True
	)

	poster_picture = VersatileImageField(
		upload_to='images/poster_picture/',
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


class Request(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	sender = models.ForeignKey(User,related_name="request_to", on_delete=models.CASCADE)
	time_creation = models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return str(self.id)


# class Account(models.Model):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


# 	def __str__(self):
# 		return str(self.id)