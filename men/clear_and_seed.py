"""
Geçici script - Tüm kullanıcıları sil ve sadece psikolog oluştur
Bu script'i çalıştırmak için: python clear_and_seed.py
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
import json
from pathlib import Path
from django.conf import settings

PSYCHOLOGIST_EMAIL = "kristin@gmail.com"
PSYCHOLOGIST_USERNAME = "kristin"
PSYCHOLOGIST_PASSWORD = "123456789aB"

# TÜM KULLANICILARI SİL (superuser hariç)
all_users = User.objects.all()
deleted_count = 0
for user in all_users:
    if not user.is_superuser:
        user.delete()
        deleted_count += 1

print(f'✓ Deleted {deleted_count} user(s) from database')

# user_data.json dosyasını temizle
storage_file = Path(settings.BASE_DIR) / 'user_data.json'
if storage_file.exists():
    try:
        with open(storage_file, 'w', encoding='utf-8') as f:
            json.dump({'users': []}, f, ensure_ascii=False, indent=2)
        print('✓ Cleared user_data.json file')
    except Exception as e:
        print(f'⚠ Could not clear user_data.json: {e}')

# Psikolog kullanıcısını oluştur
user, created = User.objects.get_or_create(
    username=PSYCHOLOGIST_USERNAME,
    defaults={'email': PSYCHOLOGIST_EMAIL}
)

# Email ve şifreyi her zaman güncelle
user.email = PSYCHOLOGIST_EMAIL
user.set_password(PSYCHOLOGIST_PASSWORD)
user.save()

if created:
    print(f'✓ Psychologist user "{PSYCHOLOGIST_USERNAME}" created successfully')
else:
    print(f'✓ Psychologist user "{PSYCHOLOGIST_USERNAME}" updated successfully')

# Profile oluştur/güncelle
profile, profile_created = Profile.objects.get_or_create(
    user=user,
    defaults={'role': 'psychologist'}
)

if not profile_created:
    profile.role = 'psychologist'
    profile.save()

print(f'✓ Profile role set to "psychologist" for user "{PSYCHOLOGIST_USERNAME}"')
print('')
print('=' * 60)
print('PSYCHOLOGIST LOGIN CREDENTIALS:')
print('=' * 60)
print(f'Username: {PSYCHOLOGIST_USERNAME}')
print(f'Email: {PSYCHOLOGIST_EMAIL}')
print(f'Password: {PSYCHOLOGIST_PASSWORD}')
print('=' * 60)
print('✓ Psychologist seeding completed!')

