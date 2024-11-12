from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render ,redirect
from django.urls import reverse
from  django.views.generic.base import View
from . import models
from .models import Question, Likes, Comment, LikesComment

from .form import CommentsForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden



class AddLikeView(View):

    def get(self, request, pk, is_like=True):
        if not request.user.is_authenticated:
            # Перенаправляем на страницу логина, если пользователь не авторизован
            return  render(request, 'blog/login.html')
        user = request.user
        question = Question.objects.get(id=pk)


        # Проверка: если пользователь уже лайкнул вопрос
        like = Likes.objects.filter(user=user, pos=question).first()
        if like:
            like.delete()
            return redirect(f'/question/{pk}')
        else:
            Likes.objects.create(user=user, pos=question,is_like=is_like)
            return redirect(f'/question/{pk}')


class AddCommentLikeView(View):

    def get(self, request, comment_id, is_like=True):
        if not request.user.is_authenticated:
            # Перенаправляем на страницу логина, если пользователь не авторизован
            return redirect('login')

        comment = Comment.objects.get(id=comment_id)

        # Проверка, если пользователь уже лайкнул/дизлайкнул комментарий
        like = LikesComment.objects.filter(user=request.user, comment=comment).first()
        if like:
            like.delete()  # Удаляем лайк, если он уже был
        else:
            try:
                LikesComment.objects.create(user=request.user, comment=comment, is_like=is_like)
            except:
                print(f"Запись с user_id={request.user} и pos_id={comment} уже существует.")
        return redirect(f'/question/{comment.question.id}')


class QuestionView(View):
    def get(self,request):
        page = paginate(models.Question.objects.new(), request, per_page=5)
        #questions =models.Question.objects.all()
        return  render(request, 'blog/index.html',{'question_list':page.object_list,'page_obj':page})

class TagView(View):
    def get(self,request):
        page = paginate(models.Question.objects.all(), request, per_page=5)
        #questions =models.Question.objects.all()
        return  render(request, 'blog/tag.html',{'question_list':page.object_list,'page_obj':page})


class QuestionDetails(View):
    """Отдельный вопрос"""
    def get(self, request, pk):
        question = Question.objects.get(id=pk)
        user_has_liked = False
        if request.user.is_authenticated:
            user_has_liked = Likes.objects.filter(user=request.user, pos=question).exists()
        like_count = question.likes_set.filter(is_like=True).count()  # Подсчёт лайков
        dislike_count = question.likes_set.filter(is_like=False).count()  # Подсчёт дизлайков
        total_likes = like_count - dislike_count
        # q=question.comment.all
        comments = paginate(question.comments.all(), request, per_page=5)
        for comment in comments:
            comment.like_count = comment.likes.filter(is_like=True).count()
            comment.dislike_count = comment.likes.filter(is_like=False).count()
            comment.total_likes = comment.like_count - comment.dislike_count

        return render(request, "blog/question_detail.html", {
            'question': question,
            'user_has_liked': user_has_liked,
            'total_likes': total_likes,
            'comments': comments.object_list,
            'page_obj': comments
        })

class HotQuestionView(View):
    def get(self,request):
        page = paginate(models.Question.objects.popular(), request, per_page=5)
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

def paginate(objects_list, request, per_page=5):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


# Create your views here.
