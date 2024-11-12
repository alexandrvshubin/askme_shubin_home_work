from django.contrib import admin
from .models import Question, Profile,Tag
from .models import Comment
from .models import Likes, LikesComment


@admin.register(Question)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','id')
    filter_horizontal = ('tags',)

@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name','question')


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('user', 'pos','is_like')

@admin.register(LikesComment)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment','is_like')
# @admin.register(Likes)
# class CommentsAdmin(admin.ModelAdmin):
#     list_display = ('ip','pos')

@admin.register(Profile)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')

@admin.register(Tag)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name',)
# Register your models here.
