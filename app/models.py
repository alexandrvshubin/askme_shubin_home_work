from django.db import models
from django.contrib.auth.models import User

class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-id')  # Новый вопрос будет с большим ID

    def popular(self):
        return self.annotate(likes_count=models.Count('likes')).order_by('-likes_count')

class Question(models.Model):
    title =models.CharField("Title Question", max_length=100)
    text=models.TextField("Text Qestion")
    tags = models.ManyToManyField('Tag', related_name='questions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', verbose_name="Автор")

    objects = QuestionManager()

    def __str__(self):
            return f"{self.title},{self.id}"


    class Meta:
        verbose_name= "Запись"
        verbose_name_plural= "Записи"

class Comment(models.Model):
    """ответ"""
    email =models.EmailField()
    name =models.CharField("Name", max_length=50)
    text_comment =models.TextField("Text Comment", max_length=2000)
    question = models.ForeignKey(Question, verbose_name="Publication", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    def __str__(self):
            return f"{self.user.username},{self.question.id}"
    class Meta:
        verbose_name= "Комментарий"
        verbose_name_plural= "Комментарии"


class Likes(models.Model):
    """Лайки"""
    # ip = models.CharField("IP-address", max_length=100, blank=True, null=True, default="0.0.0.0")
    pos = models.ForeignKey(Question, verbose_name="Публикация", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    is_like = models.BooleanField(default=True)  # True - Лайк, False - Дизлайк

    def __str__(self):
        return f"{self.user.username} лайкнул {self.pos.title}"

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        unique_together = ('user', 'pos')

class LikesComment(models.Model):
    """Лайки для комментариев"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    is_like = models.BooleanField(default=True)  # True - Лайк, False - Дизлайк

    def __str__(self):
        return f"{self.user.username} лайкнул {self.comment.text_comment}"

    class Meta:
        verbose_name = "Лайк комментария"
        verbose_name_plural = "Лайки комментариев"
        unique_together = ('user', 'comment')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name= "пользователь"
        verbose_name_plural= "пользователи"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name= "тег"
        verbose_name_plural= "теги"
# Create your models here.
