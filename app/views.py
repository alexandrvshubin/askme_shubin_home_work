from django.core.paginator import Paginator
from django.shortcuts import render ,redirect
from  django.views.generic.base import View
from . import models
from .models import Question, Likes

from .form import CommentsForm


class QuestionView(View):
    def get(self,request):
        page_num =int(request.GET.get('page',1))
        paginator = Paginator(models.Question.objects.all(),per_page=5)
        page = paginator.page(page_num)
        #questions =models.Question.objects.all()
        return  render(request, 'blog/index.html',{'question_list':page.object_list,'page_obj':page})

class TagView(View):
    def get(self,request):
        page_num =int(request.GET.get('page',1))
        paginator = Paginator(models.Question.objects.all(),per_page=5)
        page = paginator.page(page_num)
        #questions =models.Question.objects.all()
        return  render(request, 'blog/tag.html',{'question_list':page.object_list,'page_obj':page})

class QuestionDetails(View):
    """отдельный вопрос"""
    def get(self, request,pk):
        question =Question.objects.get(id=pk)
        return render(request, "blog/question_detail.html",{'question':question})

class HotQuestionView(View):
    def get(self,request):
        page_num = int(request.GET.get('page', 1))
        paginator = Paginator(list(reversed(models.Question.objects.all())), per_page=5)
        page = paginator.page(page_num)
        #questions =models.Question.objects.all()
        return  render(request, 'blog/hot.html',{'question_list':page.object_list,'page_obj':page})

class SettingsView(View):
    def get(self,request):
        return  render(request, 'blog/settings.html')

class NewAskView(View):
    def get(self,request):
        return  render(request, 'blog/ask.html')

class LoginView(View):
    def get(self,request):
        return  render(request, 'blog/login.html')

class RegisterView(View):
    def get(self,request):
        return  render(request, 'blog/register.html')

class AddComments(View):
    """Добавление комментариев"""
    def post(self, request,pk):
        form =CommentsForm(request.POST)
        if form.is_valid():
            form =form.save(commit=False)
            form.post_id =pk
            form.save()
        return redirect(f'/question/{pk}')

def get_client_ip(request):
    x_forvarded_for =request.META.get("HTTP_X_FORVARDED_FOR")
    if x_forvarded_for:
        ip =x_forvarded_for.spit(',')[0]
    else:
        ip =request.META.get("REMOTE_ADDR")
    return ip

class AddLike(View):
    def get(self, request, pk):
        ip_client =get_client_ip(request)
        try:
            Likes.objects.get(ip=ip_client,pos_id=pk)
            return redirect(f'/question/{pk}')
        except:
            new_like = Likes()
            new_like.ip = ip_client
            new_like.pos_id= int(pk)
            new_like.save()
            return  redirect(f'/question/{pk}')

class DelLike(View):
    def get(self, reuest, pk):
        ip_client =get_client_ip(reuest)
        try:
            like = Likes.objects.get(ip=ip_client)
            print(like)
            like.delete()
            return  redirect(f'/question/{pk}')
        except:
            return redirect(f'/question/{pk}')

# Create your views here.
