from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (

    PostList,
    PostDetail,

    CommentList,
    CommentDetail,

    
    ReplyList,
    ReplyDetail,

)

urlpatterns = [

    path('post-list/',PostList.as_view(), name='post-list'),
    #post-list/?search=""'
    #post-list/?following=true
    path('post-detail/<int:pk>', PostDetail.as_view(), name="post-detail"),
    

    path('post/<int:post_id>/comment-list/',CommentList.as_view(), name="comment-list" ),
    path('comment-detail/<int:pk>', CommentDetail.as_view(), name="comment-detail"),
    
    
    path('comment/<int:comment_id>/reply-list/',ReplyList.as_view(), name="reply-list"),
    path('reply-detail/<int:pk>', ReplyDetail.as_view(), name='reply-detail'),



]