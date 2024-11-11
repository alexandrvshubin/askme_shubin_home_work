from django.contrib import admin
from .models import Question, Profile,Tag
from .models import Comments
from .models import Likes


@admin.register(Question)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','id')
    filter_horizontal = ('tags',)

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name','post')

@admin.register(Likes)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('ip','pos')

@admin.register(Profile)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')

@admin.register(Tag)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name',)
# Register your models here.
