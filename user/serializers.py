


from rest_framework import serializers

from .models import *


from versatileimagefield.serializers import VersatileImageFieldSerializer

from django.contrib.auth import get_user_model
User = get_user_model()

class Profile_Simple_Serializer(serializers.ModelSerializer):
	profile_picture = VersatileImageFieldSerializer(
		sizes=[
			('full_size', 'url'),
            ('small', 'thumbnail__200x200'),
            ('medium', 'thumbnail__400x400'),
		]
	)
	poster_picture = VersatileImageFieldSerializer(
		sizes=[
			('full_size', 'url'),
            ('small', 'thumbnail__200x200'),
            ('medium', 'thumbnail__400x400'),
		]
	)
	class Meta:
		model = Profile
		fields = ['name','public_username','profile_picture','poster_picture']

class User_Serializer(serializers.ModelSerializer):
	profile = Profile_Simple_Serializer()
	
	class Meta:
		model = CustomUser
		fields = ['id','profile']

class Connection_Serializer(serializers.ModelSerializer):
	user = User_Serializer()
	class Meta:
		model = Connection
		fields = ['id','user']

class Request_Serializer(serializers.ModelSerializer):
	sender = User_Serializer()
	class Meta:
		model = Request
		fields = '__all__'

class Relationship_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Relationship
		fields = '__all__'

class Block_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Block
		fields = '__all__'