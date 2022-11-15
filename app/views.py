from .serializers import Like_Serializer
from .serializers import Reply_Serializer
from .serializers import Comment_Serializer
from .filters import PostFilter
from .serializers import Post_Serializer
from django_filters.rest_framework import DjangoFilterBackend
from http import server
from os import stat

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q

from django.core.exceptions import ValidationError

from rest_framework import generics, mixins, response, decorators, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.decorators import action
# Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


from .permissions import IsOwnerOrReadOnly
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.


class PostList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    serializer_class = Post_Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    filter_backends = {DjangoFilterBackend, }
    filterset_class = PostFilter

    # def get_queryset(self):
    # 	if 'user_id' in self.kwargs:
    # 		return Post.objects.all().filter(user=self.kwargs['user_id'])
    # 	elif 'search' in self.request.query_params:
    # 		return Post.objects.all().filter(
    # 			Q(text__icontains=self.request.query_params['search'])
    # 		)
    # 	else:
    # 		return Post.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = Post_Serializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Using generic class-based views
# https://www.django-rest-framework.org/tutorial/3-class-based-views/


class CommentList(generics.ListCreateAPIView):
    serializer_class = Comment_Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if 'post_id' in self.kwargs:
            return Comment.objects.all().filter(post=self.kwargs['post_id'])
        else:
            return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        post=Post.objects.get(id=self.kwargs['post_id']))


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = Comment_Serializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class ReplyList(generics.ListCreateAPIView):
    serializer_class = Reply_Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if 'comment_id' in self.kwargs:
            return Reply.objects.all().filter(comment=self.kwargs['comment_id'])
        else:
            return Reply.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, comment=Comment.objects.get(
            id=self.kwargs['comment_id']))


class ReplyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = Reply_Serializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# class LikeViewSet(viewsets.ModelViewSet):
#     serializer_class = Like_Serializer

#     def get_queryset(self):
#         return Like.objects.all().filter(user=self.request.user)


#     @action(detail=False,)
#     def list(self, request):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(instance=queryset, many=True)
#         return Response(serializer.data)

#     @action(detail=True,)
#     def set_like(self, request, pk=None):
#         pass





#         def get_permissions(self):
#     if self.action == 'list':
#         permission_classes = [IsAuthenticated]
#         else:
#             permission_classes = [IsAdminUser]return [permission() for permission in permission_classes]


class LikeList(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = Like_Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if 'post_id' in self.kwargs:
            return Like.objects.all().filter(post=self.kwargs['post_id'])
        elif 'comment_id' in self.kwargs:
            return Like.objects.all().filter(comment=self.kwargs['comment_id'])
        elif 'reply_id' in self.kwargs:
            return Like.objects.all().filter(reply=self.kwargs['reply_id'])
        else:
            return Like.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = Like_Serializer
    



class LikeHandler(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if 'post_id' in self.kwargs:
            return Like.objects.all().get(user=self.request.user, post=self.kwargs['post_id'])
        elif 'comment_id' in self.kwargs:
            return Like.objects.all().get(user=self.request.user, comment=self.kwargs['comment_id'])
        elif 'reply_id' in self.kwargs:
            return Like.objects.all().get(user=self.request.user, reply=self.kwargs['reply_id'])

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            queryset.delete()
            return Response("like has been deleted", status=status.HTTP_201_CREATED)
        else:
            if 'post_id' in self.kwargs:
                like = Like(user=self.request.user,
                            post=self.kwargs['post_id'])
                like.save()
            elif 'comment_id' in self.kwargs:
                like = Like(user=self.request.user,
                            comment=self.kwargs['comment_id'])
                like.save()
            elif 'reply_id' in self.kwargs:
                like = Like(user=self.request.user,
                            reply=self.kwargs['reply_id'])
                like.save()
            return Response("like has been created", status=status.HTTP_201_CREATED)


class SaveList(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = Like_Serializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Save.objects.all().filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SaveHandler(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if 'post_id' in self.kwargs:
            return Save.objects.all().get(user=self.request.user, post=self.kwargs['post_id'])

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            queryset.delete()
            return Response("Save has been deleted", status=status.HTTP_201_CREATED)
        else:
            if 'post_id' in self.kwargs:
                save = Save(user=self.request.user,
                            post=self.kwargs['post_id'])
                save.save()
            return Response("Save has been created", status=status.HTTP_201_CREATED)
