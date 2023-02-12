


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

class User_Simple_Serializer(serializers.ModelSerializer):
	profile = Profile_Simple_Serializer()
	
	class Meta:
		model = CustomUser
		fields = ['id','profile']


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
	connections_amount = serializers.IntegerField(source="get_connections_amount",required=False,read_only=True)
	is_connected = serializers.SerializerMethodField()
	is_requested = serializers.SerializerMethodField()
	# is_blocked = serializers.SerializerMethodField()
	relationship = serializers.SerializerMethodField()

	class Meta:
		model = CustomUser
		fields = ['id',
			'last_login',
			'is_superuser',
			'is_staff',
			'is_active',
			'date_joined',
			'groups',
			'user_permissions',
			'profile',
			'connections_amount',
			'is_connected',
			'is_requested',
			'relationship',
			]

	def get_is_connected(self,obj):
		# will work even no authenticated user
		if self.context['request'].user.id == None:
			return False
		elif self.context['request'].user.connection in obj.connection.connected.all():
			return True
		else:
			return False

	def get_is_requested(self,obj):
		# will work even no authenticated user
		if self.context['request'].user.id == None:
			return False
		elif obj.request_set.filter(sender=self.context['request'].user).exists():
			return True
		else:
			return False

	def get_relationship(self,obj):
		if self.context['request'].user.id == None:
			return None
		try:
			a = Relationship.objects.get(user=self.context['request'].user,to_user=obj)
		except Relationship.DoesNotExist:
			return None
		return Relationship_Serializer(instance=a).data

class my_user_serializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		# fields = '__all__'
		exclude = ('password',)
		read_only_fields = ['username','is_superuser','is_staff','is_active','date_joined','groups','user_permissions','profile']

class my_profile_serializer(serializers.ModelSerializer):
	profile_picture = VersatileImageFieldSerializer(
		sizes=[
			('full_size', 'url'),
			('thumbnail', 'thumbnail__100x100'),
			('medium_square_crop', 'crop__400x400'),
			('small_square_crop', 'crop__50x50')
		],
		required=False,
	)

	poster_picture = VersatileImageFieldSerializer(
		sizes=[
			('full_size', 'url'),
			('thumbnail', 'thumbnail__100x100'),
			('medium_square_crop', 'crop__400x400'),
			('small_square_crop', 'crop__50x50')
		],
		required=False,
	)
	class Meta:
		model = Profile
		fields = '__all__'

class Relationship_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Relationship
		exclude = ('user','to_user',)
		
class Connection_Serializer(serializers.ModelSerializer):
	user = User_Simple_Serializer()
	relationship = serializers.SerializerMethodField()
	class Meta:
		model = Connection
		fields = ['id','user','relationship']

	def get_relationship(self,obj):
		try:
			a = Relationship.objects.get(user=self.context['request'].user,to_user=obj.user)
		except Relationship.DoesNotExist:
			return None
		return Relationship_Serializer(instance=a).data

class Request_Serializer(serializers.ModelSerializer):
	user = User_Simple_Serializer()
	sender = User_Simple_Serializer()
	class Meta:
		model = Request
		fields = '__all__'



class Block_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Block
		fields = '__all__'