from django.db import models
from django.contrib.auth.models import User
import django.db.models.deletion
from django.conf import settings

# Create your models here.


class Article(models.Model):
    title = models.CharField("Başlık", max_length=50)
    content = models.CharField("Yazı", max_length=450)
    date_posted = models.DateTimeField("Tarih", auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Profile(models.Model):
    profile_pic = models.ImageField(null=True, blank=True,default='default-image.PNG',upload_to='media/')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ChatHistory(models.Model):
    history_id = models.CharField(max_length=64, blank=False, null=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)

class ChatHistoryContent(models.Model):
    role=models.CharField(choices=[('user', 'User'), ('bot', 'Bot')], max_length=10)
    content=models.TextField()
    chat_history=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.chathistory')
    likes = models.IntegerField(default=0)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(ChatHistoryContent, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'story')
