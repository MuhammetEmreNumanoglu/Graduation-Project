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
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('psychologist', 'Psychologist'),
    ]
    
    # Düzeltme: `default` değeri dosya yolunu string olarak almalıdır.
    profile_pic = models.ImageField(null=True, blank=True,default='default-image.png',upload_to='media/')
    
    # Düzeltme: Bu alan ForeignKey değil, OneToOneField olmalı ki her kullanıcının tek bir profili olsun.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Role alanı: 'member' veya 'psychologist'
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')

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


# ==========================================================
# === PSİKOLOG SİSTEMİ MODELLERİ ===
# ==========================================================

class Task(models.Model):
    """Psikolog tarafından üyelere gönderilen görevler"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Task for {self.user.username} - {self.text[:50]}"


class Notification(models.Model):
    """Psikolog tarafından üyelere gönderilen bildirimler"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username} - {self.text[:50]}"


class PsychologistMessage(models.Model):
    """Psikolog ve üyeler arasındaki mesajlaşma"""
    SENDER_CHOICES = [
        ('user', 'User'),
        ('psychologist', 'Psychologist'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='psychologist_messages')
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender} -> {self.user.username}: {self.text[:50]}"


class LoginActivity(models.Model):
    """Kullanıcı giriş aktivitelerini takip eder - aktif günler için"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='login_activities')
    login_date = models.DateField(auto_now_add=True)  # Sadece tarih, saat yok
    
    class Meta:
        unique_together = ('user', 'login_date')  # Aynı gün için tek kayıt
        ordering = ['-login_date']
        indexes = [
            models.Index(fields=['user', 'login_date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.login_date}"