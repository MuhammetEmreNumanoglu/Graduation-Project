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

    profile_pic = models.ImageField(null=True, blank=True, default='default-image.png', upload_to='media/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    life_story = models.TextField(null=True, blank=True)


class DailyMood(models.Model):
    MOOD_CHOICES = [
        ('very_good', 'Çok iyi'),
        ('good', 'İyi'),
        ('neutral', 'Nötr'),
        ('bad', 'Kötü'),
        ('very_bad', 'Çok kötü'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='daily_moods')
    date = models.DateField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    note = models.CharField(max_length=280, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.get_mood_display()}"


class ChatHistory(models.Model):
    history_id = models.CharField(max_length=64, blank=False, null=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)


class ChatHistoryContent(models.Model):
    role = models.CharField(choices=[('user', 'User'), ('assistant', 'Assistant')], max_length=10)
    content = models.TextField()
    chat_history = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.chathistory')
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
# === GELİŞMİŞ AI HAFIZA MODELİ ===
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
    """Psikolog tarafından üyelere gönderilen görevler (kart tabanlı)"""
    TASK_TYPE_CHOICES = [
        ('breathing_exercise', 'Nefes Egzersizi'),
        ('meditation', 'Meditasyon'),
        ('daily_cards', 'Günlük Kartlar'),
        ('support_wall', 'Destek Duvarı'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    # text alanı artık görev tipi anahtarını (ör. 'breathing_exercise') tutar
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Task for {self.user.username} - {self.text[:50]}"

    def get_task_type_display_name(self):
        """Görev tipi anahtarından Türkçe display ismini döner."""
        display_map = dict(self.TASK_TYPE_CHOICES)
        return display_map.get(self.text, self.text)
        
    def get_url(self):
        """Görev tipine göre yönlendirilecek URL'yi döner."""
        route_map = {
            'breathing_exercise': '/nefes-egzersizi',
            'meditation': '/meditasyon',
            'daily_cards': '/gunluk-kartlar',
            'support_wall': '/destek-duvari',
        }
        return route_map.get(self.text, '#')


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
    login_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'login_date')
        ordering = ['-login_date']
        indexes = [
            models.Index(fields=['user', 'login_date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.login_date}"


# ==========================================================
# === PSİKOLOG-KULLANICI İLİŞKİ MODELİ ===
# ==========================================================

class PsychologistUserRelation(models.Model):
    """
    Psikolog ile kullanıcı arasındaki ilişki modeli.
    category ve private_notes burada tutulur.
    """
    CATEGORY_CHOICES = [
        ('acil', 'Acil'),
        ('supheli', 'Takip'),   # "Şüpheli" → "Takip" olarak güncellendi
        ('normal', 'Normal'),
    ]

    psychologist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='managed_users',
        verbose_name='Psikolog'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='psychologist_relations',
        verbose_name='Kullanıcı'
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='normal',
        verbose_name='Kategori'
    )
    private_notes = models.TextField(
        null=True,
        blank=True,
        verbose_name='Kişiye Özel Notlar'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('psychologist', 'user')
        ordering = ['-updated_at']
        verbose_name = 'Psikolog-Kullanıcı İlişkisi'
        verbose_name_plural = 'Psikolog-Kullanıcı İlişkileri'

    def __str__(self):
        return f"{self.psychologist.username} → {self.user.username} [{self.category}]"


# ==========================================================
# === SEANS DEĞERLENDİRME MODELİ ===
# ==========================================================

class SessionRating(models.Model):
    """Psikolog tarafından her kullanıcı için günlük seans değerlendirmesi (1-10)"""
    psychologist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_ratings',
        verbose_name='Psikolog'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_ratings',
        verbose_name='Kullanıcı'
    )
    rating = models.IntegerField(verbose_name='Değerlendirme (1-10)')
    note = models.TextField(null=True, blank=True, verbose_name='Seans Notu')
    session_date = models.DateField(verbose_name='Seans Tarihi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('psychologist', 'user', 'session_date')
        ordering = ['-session_date']
        verbose_name = 'Seans Değerlendirmesi'
        verbose_name_plural = 'Seans Değerlendirmeleri'

    def __str__(self):
        return f"{self.psychologist.username} → {self.user.username} [{self.session_date}]: {self.rating}/10"


# ==========================================================
# === FORUM (DESTEK DUVARI) MODELLERİ ===
# ==========================================================

class ForumPost(models.Model):
    """Destek Duvarı / Forum gönderileri"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='forum_posts'
    )
    content = models.TextField(verbose_name='İçerik')
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Forum Gönderisi'
        verbose_name_plural = 'Forum Gönderileri'

    def __str__(self):
        return f"{self.user.username}: {self.content[:60]}"


class ForumComment(models.Model):
    """Forum gönderisine anonim yorumlar"""
    post = models.ForeignKey(
        ForumPost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='forum_comments'
    )
    content = models.TextField(verbose_name='Yorum')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Forum Yorumu'
        verbose_name_plural = 'Forum Yorumları'

    def __str__(self):
        return f"Comment on post #{self.post.id}: {self.content[:40]}"


class ForumLike(models.Model):
    """Kullanıcı başına forum beğenisi — tekrarlı beğeni yok"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='forum_likes'
    )
    post = models.ForeignKey(
        ForumPost,
        on_delete=models.CASCADE,
        related_name='post_likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = 'Forum Beğenisi'
        verbose_name_plural = 'Forum Beğenileri'

    def __str__(self):
        return f"{self.user.username} liked post #{self.post.id}"