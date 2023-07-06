from rest_framework import serializers
from ..models import *
from versatileimagefield.serializers import VersatileImageFieldSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class Profile_Simple_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Profile
		fields = ['name','public_username']

class User_Serializer(serializers.ModelSerializer):
	profile = Profile_Simple_Serializer(required=False)
	username = serializers.CharField(write_only=True,required=False)	# required false for update
	password = serializers.CharField(write_only=True,required=False)	# required false for update
	confirm_password = serializers.CharField(write_only=True,required=False)	# required false for update


	class Meta:
		model = CustomUser
		fields = ['id','profile','is_staff','username','email','phone_number','email_verified','password','confirm_password','is_superuser','is_active','last_login','date_joined']

	def create(self,validated_data):
		username = validated_data["username"]
		email = validated_data["email"]
		password = validated_data["password"]
		confirm_password = validated_data["confirm_password"]
		phone_number = validated_data.get("phone_number") # Use get() method to handle the case when phone_number is not provided
		if password != confirm_password:
			raise serializers.ValidationError("The two passwords differ")
		user = User(username=username, email=email,phone_number=phone_number)
		user.set_password(password)
		user.save()
		return user

	def update(self, instance, validated_data):
		# Use get() method to handle the case when username is not provided
		instance.username = validated_data.get('username', instance.username)
		instance.email = validated_data.get('email', instance.email)
		instance.phone_number = validated_data.get('phone_number', instance.phone_number)

		password = validated_data.get('password')
		confirm_password = validated_data.get('confirm_password')
		if password and password != confirm_password:
			raise serializers.ValidationError("The two passwords differ")
		if password:
			instance.set_password(password)

		instance.save()
		return instance
