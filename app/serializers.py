from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


from versatileimagefield.serializers import VersatileImageFieldSerializer

from user.serializers import User_Serializer


class PostList_Serializer(serializers.ModelSerializer):
    user = User_Serializer(required=False)
    likes_amount = serializers.IntegerField(source="get_likes_amount")
    comments_amount = serializers.IntegerField(source="get_comments_amount")
    # shares_amount =
    # liked = serializers.SerializerMethodField()
    # shared =
    # saved =

    class Meta:
        model = Post
        fields = ['id', 'user', 'text', 'time_creation',
            'likes_amount', 'comments_amount']
        read_only_fields = ['user']

	# def get_liked(self,obj):
	# 	if obj.like_set


class PostDetail_Serializer(serializers.ModelSerializer):
    user = User_Serializer(required=False)
    likes_amount = serializers.IntegerField(source="get_likes_amount")
    comments_amount = serializers.IntegerField(source="get_comments_amount")
    # likes_amount = serializers.
    # comments_amount =
    # shares_amount =
    # liked =
    # shared =
    # saved =
    class Meta:
        model = Post
        fields = ['id','user','text','time_creation','likes_amount','comments_amount']
        read_only_fields = ['user']


class CommentList_Serializer(serializers.ModelSerializer):
    user = User_Serializer(required=False)
    likes_amount = serializers.IntegerField(source="get_likes_amount")
    # likes_amount =
    # liked =
    class Meta:
        model = Comment
        fields = ['post','user','text','time_creation','likes_amount']
        read_only_fields = ['user', 'post']


class CommentDetail_Serializer(serializers.ModelSerializer):
    user = User_Serializer(required=False)
    likes_amount = serializers.IntegerField(source="get_likes_amount")
    # likes_amount =
    # liked =
    class Meta:
        model = Comment
        fields = ['post','user','text','time_creation','likes_amount']
        read_only_fields = ['user', 'post']


class ReplyList_Serializer(serializers.ModelSerializer):
    user = User_Serializer(required=False)
    likes_amount = serializers.IntegerField(source="get_likes_amount")
    # likes_amount =
    # liked =
    class Meta:
        model = Reply
        fields = ['comment','user','text','time_creation','likes_amount']
        read_only_fields = ['user', 'comment']


class ReplyDetail_Serializer(serializers.ModelSerializer):
    user = User_Serializer(required=False)
    likes_amount = serializers.IntegerField(source="get_likes_amount")
    # likes_amount =
    # liked =
    class Meta:
        model = Reply
        fields = ['comment','user','text','time_creation','likes_amount']
        read_only_fields = ['user', 'comment']
