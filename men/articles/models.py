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

    # YENİ TEST ALANI: Lütfen bu satırı ekleyin
    test_alani = models.CharField(max_length=10, null=True, blank=True)


class Profile(models.Model):
    # Düzeltme: `default` değeri dosya yolunu string olarak almalıdır.
    profile_pic = models.ImageField(null=True, blank=True,default='default-image.png',upload_to='media/')
    
    # Düzeltme: Bu alan ForeignKey değil, OneToOneField olmalı ki her kullanıcının tek bir profili olsun.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class ChatHistory(models.Model):
    history_id = models.CharField(max_length=64, blank=False, null=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)

class ChatHistoryContent(models.Model):
    # Düzeltme: Bot rolü için 'assistant' daha standart bir isimlendirmedir.
    role=models.CharField(choices=[('user', 'User'), ('assistant', 'Assistant')], max_length=10)
    content=models.TextField()
    chat_history=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.chathistory')
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(ChatHistoryContent, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'story')


class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_contacts')
    relation = models.CharField(max_length=64)
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.relation})"

# ==========================================================
# === YENİ EKLENEN GELİŞMİŞ AI HAFIZA MODELİ ===
# ==========================================================
class UserAIAssistantProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_profile')
    long_term_memory = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Profile for {self.user.username}"