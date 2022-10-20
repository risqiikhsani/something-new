from django.contrib import admin

from .models import Post, Comment, Reply, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'time_creation')    
    list_filter = ('user', 'time_creation')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'text', 'time_creation')
    list_filter = ('post', 'user', 'time_creation')


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user', 'text', 'time_creation')
    list_filter = ('comment', 'user', 'time_creation')        


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'post',
        'comment',
        'reply',
        'time_creation',
    )
    list_filter = ('user', 'post', 'comment', 'reply', 'time_creation')