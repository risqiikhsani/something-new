import json
from queue import Empty
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


from versatileimagefield.serializers import VersatileImageFieldSerializer

from user.serializers import User_Serializer

class PostMedia_Serializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
            ('medium_square_crop', 'crop__400x400'),
            ('small_square_crop', 'crop__50x50')
        ],
    )
    class Meta:
        model = PostMedia
        fields = ['id','post','image','time_creation']
        read_only_fields = ['post']

class ListFieldWithSaneDefault(serializers.ListField):
    """
    This is used ONLY as a base class for other fields.  When using it, please ensure that you
    always provide a default value (at least `default=lambda: []`) if the field is not required.
    Your derived class should take no parameters to __init__, it should be self contained
    """
    def get_value(self, dictionary):
        """
        When handling html multipart forms input (as opposed to json, which works properly)
        the base list field returns `[]` for _missing_ keys.  This override checks for that specific
        case and returns `empty` so that standard default-value processing takes over
        """
        if self.field_name not in dictionary:
            return Empty
        return super(ListFieldWithSaneDefault, self).get_value(dictionary)
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
    # delete_images_id = serializers.ListField(required=False,child=serializers.IntegerField(),write_only=True,allow_empty=True, min_length=None, max_length=None)
    delete_images_id = serializers.JSONField(required=False,write_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'text', 'time_creation','natural_time','natural_day',
            'likes_amount', 'comments_amount','shares_amount','liked','shared','saved','postmedia_set','delete_images_id']
        read_only_fields = ['user','postmedia_set']
        # extra_kwargs = [
        #     'deleted_images_id':{'write_only':True}, 
        # ]


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
            print(i.size)

        a = Post.objects.create(**validated_data)
        for i in self.context['request'].FILES.values():
            b = PostMedia.objects.create(post=a,image=i)
            b.save()
        return a
    
    def validate(self,data):
        limit = 8 * 1024 * 1024
        totalsize = 0
        for i in self.context['request'].FILES.values():
            print(i)
            print(i.size)
            totalsize = totalsize + i.size
        if totalsize > limit:
            raise serializers.ValidationError({'File too large. Total file Size should not exceed 8 MiB.'})
        return data

    def update(self,instance,validated_data):
        instance.text = validated_data.get('text',instance.text)
        for i in self.context['request'].FILES.values():
            b = PostMedia.objects.create(post=instance,image=i)
            b.save()
        if "delete_images_id" in validated_data:
            for a in validated_data['delete_images_id']:
                print(a)
                try:
                    z = PostMedia.objects.get(id=a)
                    z.delete()
                except PostMedia.DoesNotExist:
                    pass
        instance.save()
        return instance





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

