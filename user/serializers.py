


from rest_framework import serializers

from .models import *


from versatileimagefield.serializers import VersatileImageFieldSerializer



class Profile_Serializer(serializers.ModelSerializer):
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
		fields = ['name','public_username','about','profile_picture','poster_picture']

class User_Serializer(serializers.ModelSerializer):
	profile = Profile_Serializer()
	
	class Meta:
		model = CustomUser
		fields = ['id','profile']