from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


from versatileimagefield.serializers import VersatileImageFieldSerializer

from user.serializers import User_Serializer


class Post_Serializer(serializers.ModelSerializer):
    user = User_Serializer(required=False)
    likes_amount = serializers.IntegerField(source="get_likes_amount",required=False)
    comments_amount = serializers.IntegerField(source="get_comments_amount",required=False)
    shares_amount = serializers.IntegerField(source="get_shares_amount",required=False)
    liked = serializers.SerializerMethodField()
    shared = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'text', 'time_creation',
            'likes_amount', 'comments_amount','shares_amount','liked','shared','saved']
        read_only_fields = ['user',]

    def get_liked(self,obj):
        # will work even no authenticated user
        if self.context['request'].user.id == None:
            return False
        elif obj.like_set.all().filter(user=self.context['request'].user).exists():
            return True
        else:
            return False

    def get_shared(self,obj):
        if self.context['request'].user.id == None:
            return False
        elif obj.share_set.all().filter(user=self.context['request'].user).exists():
            return True
        else:
            return False

    def get_saved(self,obj):
        if self.context['request'].user.id == None:
            return False
        elif obj.save_set.all().filter(user=self.context['request'].user).exists():
            return True
        else:
            return False






class Comment_Serializer(serializers.ModelSerializer):
    user = User_Serializer(required=False)
    likes_amount = serializers.IntegerField(source="get_likes_amount",required=False)
    replies_amount = serializers.IntegerField(source="get_replies_amount",required=False)
    liked = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['post','user','text','time_creation','likes_amount','replies_amount','liked']
        read_only_fields = ['user', 'post']

    def get_liked(self,obj):
        if self.context['request'].user.id == None:
            return False
        elif obj.like_set.all().filter(user=self.context['request'].user).exists():
            return True
        else:
            return False



class Reply_Serializer(serializers.ModelSerializer):
    user = User_Serializer(required=False)
    likes_amount = serializers.IntegerField(source="get_likes_amount",required=False)
    liked = serializers.SerializerMethodField()
    class Meta:
        model = Reply
        fields = ['comment','user','text','time_creation','likes_amount','liked']
        read_only_fields = ['user', 'comment']

    def get_liked(self,obj):
        if self.context['request'].user.id == None:
            return False
        elif obj.like_set.all().filter(user=self.context['request'].user).exists():
            return True
        else:
            return False


class Like_Serializer(serializers.ModelSerializer):
    user = User_Serializer(required=False)

    class Meta:
        model = Like
        fields = ['user']
        read_only_fields = ['user']

