from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    title =models.CharField("Title Question", max_length=100)
    text=models.TextField("Text Qestion")
    img = models.ImageField("Image", upload_to='image/q_img')
    tags = models.ManyToManyField('Tag', related_name='questions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', verbose_name="Автор")

    def __str__(self):
            return f"{self.title},{self.id}"

    class Meta:
        verbose_name= "Запись"
        verbose_name_plural= "Записи"

class Comments(models.Model):
    """ответ"""
    email =models.EmailField()
    name =models.CharField("Name", max_length=50)
    text_comment =models.TextField("Text Comment", max_length=2000)
    post = models.ForeignKey(Question,verbose_name="Publication",on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    def __str__(self):
            return f"{self.name},{self.post}"
    class Meta:
        verbose_name= "Комментарий"
        verbose_name_plural= "Комментарии"



class Likes(models.Model):
    """лайки"""
    ip = models.CharField("IP-addres", max_length=100)
    pos = models.ForeignKey(Question, verbose_name="Publication",on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', blank=True, null=True)
    def __str__(self):
            return f"{self.ip},{self.pos}"
    class Meta:
        verbose_name= "лайки"
        verbose_name_plural= "лайк"

class Dislikes(models.Model):
    """лайки"""
    ip = models.CharField("IP-addres", max_length=100)
    pos = models.ForeignKey(Question, verbose_name="Publication",on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes', blank=True, null=True)
    def __str__(self):
            return f"{self.ip},{self.pos}"
    class Meta:
        verbose_name= "дизлайки"
        verbose_name_plural= "дизлайк"


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
