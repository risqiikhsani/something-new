from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (

    PostList,
    PostDetail,

    CommentList,
    CommentDetail,
    
    ReplyList,
    ReplyDetail,

    LikeList,
    LikeHandler,

    SaveList,
    SaveHandler,
)

urlpatterns = [

    path('posts',PostList.as_view(), name='post-list'),
    #post-list/?search=""'
    #post-list/?following=true
    path('post/<int:pk>', PostDetail.as_view(), name="post-detail"),
    

    path('post/<int:post_id>/comments',CommentList.as_view(), name="comment-list" ),
    path('comment/<int:pk>', CommentDetail.as_view(), name="comment-detail"),
    
    
    path('comment/<int:comment_id>/replies',ReplyList.as_view(), name="reply-list"),
    path('reply/<int:pk>', ReplyDetail.as_view(), name='reply-detail'),


    path('post/<int:post_id>/likes', LikeList.as_view(), name='like-list-post'),
    path('comment/<int:comment_id>/likes', LikeList.as_view(), name='like-list-comment'),
    path('reply/<int:reply_id>/likes', LikeList.as_view(), name='like-list-reply'),
    
    path('post/<int:post_id>/likehandler', LikeHandler.as_view(), name='like-handler-post'),
    path('comment/<int:comment_id>/likehandler', LikeHandler.as_view(), name='like-handler-comment'),
    path('reply/<int:reply_id>/likehandler', LikeHandler.as_view(), name='like-handler-reply'),

    path('saved-items/',SaveList.as_view(), name='save-list'),

    path('post/<int:post_id>/savehandler', SaveHandler.as_view(), name='save-handler-post'),
    # path('comment/<int:comment_id>/savehandler', SaveHandler.as_view(), name='save-handler-comment'),
    # path('reply/<int:reply_id>/savehandler', SaveHandler.as_view(), name='save-handler-reply'),

]