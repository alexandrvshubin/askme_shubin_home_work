from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from .models import Question, Likes, Comment, LikesComment, Tag
from .form import CommentsForm, RegisterForm, LoginForm, QuestionForm, ProfileEditForm, UserEditForm
from django.http import JsonResponse
import json






class QuestionView(View):
    def get(self, request):
        page = paginate(Question.objects.new(), request, per_page=5)
        return render(request, 'blog/index.html', {'question_list': page.object_list, 'page_obj': page})


class TagView(View):
    def get(self, request):
        page = paginate(Question.objects.all(), request, per_page=5)
        return render(request, 'blog/tag.html', {'question_list': page.object_list, 'page_obj': page})


class QuestionDetails(View):
    def get(self, request, pk):
        question = Question.objects.get(id=pk)
        user_has_liked = False
        if request.user.is_authenticated:
            user_has_liked = Likes.objects.filter(user=request.user, pos=question).exists()
        like_count = question.likes_set.filter(is_like=True).count()
        dislike_count = question.likes_set.filter(is_like=False).count()
        total_likes = like_count - dislike_count

        # Пагинация комментариев
        comments = paginate(question.comments.all(), request, per_page=5)
        for comment in comments:
            comment.like_count = comment.likes.filter(is_like=True).count()
            comment.dislike_count = comment.likes.filter(is_like=False).count()
            comment.total_likes = comment.like_count - comment.dislike_count

        form = CommentsForm()  # Форма для добавления комментария
        return render(request, "blog/question_detail.html", {
            'question': question,
            'user_has_liked': user_has_liked,
            'total_likes': total_likes,
            'comments': comments.object_list,
            'page_obj': comments,
            'form': form
        })

    @method_decorator(login_required)
    def post(self, request, pk):
        question = Question.objects.get(pk=pk)
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.question = question
            comment.save()
            return redirect('question_detail', pk=pk)

        user_has_liked = False
        if request.user.is_authenticated:
            user_has_liked = Likes.objects.filter(user=request.user, pos=question).exists()
        like_count = question.likes_set.filter(is_like=True).count()
        dislike_count = question.likes_set.filter(is_like=False).count()
        total_likes = like_count - dislike_count

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
            'page_obj': comments,
            'form': form
        })



    @method_decorator(login_required)
    def post(self, request, pk):
        question = Question.objects.get(pk=pk)
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.question = question
            comment.save()
            return redirect('question_detail', pk=pk)
        return render(request, 'blog/question_detail.html', {'question': question, 'form': form})


class HotQuestionView(View):
    def get(self, request):
        page = paginate(Question.objects.popular(), request, per_page=5)
        return render(request, 'blog/hot.html', {'question_list': page.object_list, 'page_obj': page})


class SettingsView(View):
    def get(self, request):
        return render(request, 'blog/settings.html')


@method_decorator(login_required, name='dispatch')
class ProfileEditView(View):
    def get(self, request):

        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'blog/settings.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('settings')

        return render(request, 'blog/settings.html', {'user_form': user_form, 'profile_form': profile_form})


@method_decorator(login_required, name='dispatch')
class NewAskView(View):
    def get(self, request):
        form = QuestionForm()
        return render(request, 'blog/ask.html', {'form': form})

    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()

            tags = form.cleaned_data['tags'].split(',')
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                question.tags.add(tag)

            return redirect('question_detail', pk=question.id)
        return render(request, 'blog/ask.html', {'form': form})




class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('index')
            else:
                form.add_error('password', 'Invalid username or password.')
        return render(request, 'blog/login.html', {'form': form})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'blog/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        return render(request, 'blog/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')






@login_required
def users_create(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))





class AddComments(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        question = Question.objects.get(pk=pk)
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.question = question
            comment.save()
            return redirect('question_detail', pk=pk)
        return render(request, 'blog/question_detail.html', {'question': question, 'form': form})



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






class LikeQuestionAjaxView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        try:
            data = json.loads(request.body)
            question_id = data.get('id')
            is_like = data.get('is_like') == True
            print(data.get('is_like'))

            question = Question.objects.get(id=question_id)

            like = Likes.objects.filter(user=request.user, pos=question).first()
            if like:
                like.delete()
            else:
                Likes.objects.create(user=request.user, pos=question, is_like=is_like)



            like_count = question.likes_set.filter(is_like=True).count()
            dislike_count = question.likes_set.filter(is_like=False).count()
            total_likes = like_count - dislike_count
            return JsonResponse({'total_likes': total_likes})
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

class LikeCommentAjaxView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        try:
            data = json.loads(request.body)
            comment_id = data.get('id')
            is_like = data.get('is_like') == True
            print(data.get('is_like'))

            comment = Comment.objects.get(id=comment_id)

            # Проверка, если пользователь уже лайкнул/дизлайкнул комментарий
            like = LikesComment.objects.filter(user=request.user, comment=comment).first()
            if like:
                like.delete()
            else:
                LikesComment.objects.create(user=request.user, comment=comment, is_like=is_like)


            like_count = comment.likes.filter(is_like=True).count()
            dislike_count = comment.likes.filter(is_like=False).count()
            total_likes = like_count - dislike_count

            return JsonResponse({'total_likes': total_likes})
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Comment not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

class MarkCorrectAnswerView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        try:
            data = json.loads(request.body)
            comment_id = data.get('comment_id')
            comment = Comment.objects.get(id=comment_id)

            if comment.question.user != request.user:
                return JsonResponse({'error': 'Permission denied'}, status=403)




            if comment.is_correct == False:
                comment.is_correct = True
            else:
                comment.is_correct = False
            comment.save()

            return JsonResponse({'success': True, 'comment_id': comment_id})
        except Comment.DoesNotExist:
            return JsonResponse({'error': 'Comment not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
