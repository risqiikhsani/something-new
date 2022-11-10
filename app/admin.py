from django.contrib import admin

from .models import Post, Save, Share, Comment, Reply, Report, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'time_creation')
    list_filter = ('user', 'time_creation')


@admin.register(Save)
class SaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    list_filter = ('user', 'post')


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    list_filter = ('user', 'post')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'text', 'time_creation')
    list_filter = ('post', 'user', 'time_creation')


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user', 'text', 'time_creation')
    list_filter = ('comment', 'user', 'time_creation')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'to_user',
        'to_post',
        'to_comment',
        'to_reply',
    )
    list_filter = ('user', 'to_user', 'to_post', 'to_comment', 'to_reply')


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