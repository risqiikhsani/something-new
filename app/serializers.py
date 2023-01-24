from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


from versatileimagefield.serializers import VersatileImageFieldSerializer

from user.serializers import User_Serializer

from versatileimagefield.serializers import VersatileImageFieldSerializer
class PostMedia_Serializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
            ('medium_square_crop', 'crop__400x400'),
            ('small_square_crop', 'crop__50x50')
        ]
    )
    class Meta:
        model = PostMedia
        fields = ['id','post','image','time_creation']
        read_only_fields = ['post']
class Post_Serializer(serializers.ModelSerializer):
    user = User_Serializer(required=False)
    likes_amount = serializers.IntegerField(source="get_likes_amount",required=False)
    comments_amount = serializers.IntegerField(source="get_comments_amount",required=False)
    shares_amount = serializers.IntegerField(source="get_shares_amount",required=False)
    natural_time = serializers.CharField(source="get_natural_time",required=False)
    natural_day = serializers.CharField(source="get_natural_day",required=False)
    liked = serializers.SerializerMethodField()
    shared = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()
    postmedia_set = PostMedia_Serializer(many=True,required=False)

    class Meta:
        model = Post
        fields = ['id', 'user', 'text', 'time_creation','natural_time','natural_day',
            'likes_amount', 'comments_amount','shares_amount','liked','shared','saved','postmedia_set']
        read_only_fields = ['user','postmedia_set']

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

    def create(self,validated_data):
        for i in validated_data:
            print(i)

        for i in self.context['request'].FILES.values():
            print(i)

        a = Post.objects.create(**validated_data)
        return a






class Comment_Serializer(serializers.ModelSerializer):
    user = User_Serializer(required=False)
    likes_amount = serializers.IntegerField(source="get_likes_amount",required=False)
    replies_amount = serializers.IntegerField(source="get_replies_amount",required=False)
    natural_time = serializers.CharField(source="get_natural_time",required=False)
    natural_day = serializers.CharField(source="get_natural_day",required=False)
    liked = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id','post','user','text','time_creation','natural_time','natural_day','likes_amount','replies_amount','liked']
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
    natural_time = serializers.CharField(source="get_natural_time",required=False)
    natural_day = serializers.CharField(source="get_natural_day",required=False)
    liked = serializers.SerializerMethodField()
    class Meta:
        model = Reply
        fields = ['id','comment','user','text','time_creation','natural_time','natural_day','likes_amount','liked']
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

