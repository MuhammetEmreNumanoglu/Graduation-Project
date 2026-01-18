"""
Hızlı psikolog kullanıcı oluşturma scripti
Bu script'i çalıştırmak için: python create_psychologist_now.py
"""
import os
import sys
import django

# Django'yu ayarla
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'men.settings')
django.setup()

from django.contrib.auth.models import User
from articles.models import Profile

PSYCHOLOGIST_USERNAME = "kristin"
PSYCHOLOGIST_EMAIL = "kristin@gmail.com"
PSYCHOLOGIST_PASSWORD = "123456789aB"

print("=" * 60)
print("PSİKOLOG KULLANICI OLUŞTURMA")
print("=" * 60)

# Kullanıcıyı oluştur veya güncelle
user, created = User.objects.get_or_create(
    username=PSYCHOLOGIST_USERNAME,
    defaults={'email': PSYCHOLOGIST_EMAIL}
)

# Email ve şifreyi her zaman güncelle
user.email = PSYCHOLOGIST_EMAIL
user.set_password(PSYCHOLOGIST_PASSWORD)
user.is_active = True
user.save()

if created:
    print(f"✓ Kullanıcı oluşturuldu: {user.username}")
else:
    print(f"✓ Kullanıcı güncellendi: {user.username}")

# Profile oluştur veya güncelle
profile, profile_created = Profile.objects.get_or_create(
    user=user,
    defaults={'role': 'psychologist'}
)

if not profile_created:
    profile.role = 'psychologist'
    profile.save()
    print(f"✓ Profile role güncellendi: psychologist")
else:
    print(f"✓ Profile oluşturuldu: psychologist")

# Test: Şifre kontrolü
if user.check_password(PSYCHOLOGIST_PASSWORD):
    print(f"✓ Şifre doğrulandı!")
else:
    print(f"✗ Şifre doğrulanamadı!")

print("")
print("=" * 60)
print("GİRİŞ BİLGİLERİ")
print("=" * 60)
print(f"Username: {PSYCHOLOGIST_USERNAME}")
print(f"Email: {PSYCHOLOGIST_EMAIL}")
print(f"Password: {PSYCHOLOGIST_PASSWORD}")
print("=" * 60)
print("✓ Tamamlandı! Şimdi /psychologist-login/ sayfasından giriş yapabilirsiniz.")

