from django.db import models

class Question(models.Model):
    title =models.CharField("Title Question", max_length=100)
    text=models.TextField("Text Qestion")
    id_question=models.CharField("ID Question", max_length=100)
    img = models.ImageField("Image", upload_to='image/q_img')

    def __str__(self):
            return f"{self.title},{self.id_question}"

    class Meta:
        verbose_name= "Запись"
        verbose_name_plural= "Записи"

class Comments(models.Model):
    """ответ"""
    email =models.EmailField()
    name =models.CharField("Name", max_length=50)
    text_comment =models.TextField("Text Comment", max_length=2000)
    post = models.ForeignKey(Question,verbose_name="Publication",on_delete=models.CASCADE)
    def __str__(self):
            return f"{self.name},{self.post}"
    class Meta:
        verbose_name= "Комментарий"
        verbose_name_plural= "Комментарии"


class Likes(models.Model):
    """лайки"""
    ip = models.CharField("IP-addres", max_length=100)
    pos = models.ForeignKey(Question, verbose_name="Publication",on_delete=models.CASCADE)
    def __str__(self):
            return f"{self.ip},{self.pos}"
    class Meta:
        verbose_name= "лайки"
        verbose_name_plural= "лайк"

# Create your models here.
