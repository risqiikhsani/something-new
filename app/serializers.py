from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


from versatileimagefield.serializers import VersatileImageFieldSerializer

from user.serializers import User_Serializer

class PostList_Serializer(serializers.ModelSerializer):
	user = User_Serializer()
	class Meta:
		model = Post
		fields = '__all__'
		read_only_fields = ['user']

class PostDetail_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = '__all__'
		read_only_fields = ['user']


class CommentList_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'
		read_only_fields = ['user','post']

class CommentDetail_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'
		read_only_fields = ['user','post']

class ReplyList_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Reply
		fields = '__all__'
		read_only_fields = ['user','comment']

class ReplyDetail_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Reply
		fields = '__all__'
		read_only_fields = ['user','comment']