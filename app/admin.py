from django.contrib import admin
from .models import Question
from .models import Comments
from .models import Likes


@admin.register(Question)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','id_question')

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name','post')

@admin.register(Likes)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('ip','pos')
# Register your models here.
