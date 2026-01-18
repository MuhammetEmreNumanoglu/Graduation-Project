"""
Django management command to seed the psychologist user.

Usage:
    python manage.py seed_psychologist
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from articles.models import Profile
import json
import os
from pathlib import Path
from django.conf import settings
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Deletes all users and creates only the psychologist user (kristin)'

    def handle(self, *args, **options):
        PSYCHOLOGIST_EMAIL = "kristin@gmail.com"
        PSYCHOLOGIST_USERNAME = "kristin"  # Küçük harf
        PSYCHOLOGIST_PASSWORD = "123456789aB"
        
        # TÜM KULLANICILARI SİL (superuser hariç)
        all_users = User.objects.all()
        deleted_count = 0
        for user in all_users:
            # Superuser'ları silme
            if not user.is_superuser:
                user.delete()
                deleted_count += 1
        
        self.stdout.write(self.style.WARNING(f'Deleted {deleted_count} user(s) from database'))
        
        # user_data.json dosyasını da temizle
        storage_file = Path(settings.BASE_DIR) / 'user_data.json'
        if storage_file.exists():
            try:
                with open(storage_file, 'w', encoding='utf-8') as f:
                    json.dump({'users': []}, f, ensure_ascii=False, indent=2)
                self.stdout.write(self.style.WARNING('Cleared user_data.json file'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Could not clear user_data.json: {e}'))
        
        # Psikolog kullanıcısını oluştur
        user, created = User.objects.get_or_create(
            username=PSYCHOLOGIST_USERNAME,
            defaults={
                'email': PSYCHOLOGIST_EMAIL,
            }
        )
        
        # Email ve şifreyi her zaman güncelle
        user.email = PSYCHOLOGIST_EMAIL
        user.set_password(PSYCHOLOGIST_PASSWORD)
        user.save()
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Psychologist user "{PSYCHOLOGIST_USERNAME}" created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Psychologist user "{PSYCHOLOGIST_USERNAME}" updated successfully'))
        
        # Profile oluştur/güncelle
        profile, profile_created = Profile.objects.get_or_create(
            user=user,
            defaults={'role': 'psychologist'}
        )
        
        if not profile_created:
            profile.role = 'psychologist'
            profile.save()
        
        self.stdout.write(self.style.SUCCESS(f'Profile role set to "psychologist" for user "{PSYCHOLOGIST_USERNAME}"'))
        
        # user_data.json dosyasına da psikolog bilgilerini ekle
        storage_file = Path(settings.BASE_DIR) / 'user_data.json'
        try:
            if storage_file.exists():
                with open(storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {'users': []}
            
            # Mevcut psikolog kullanıcısını kontrol et ve güncelle
            users = data.get('users', [])
            psychologist_found = False
            
            for u in users:
                if u.get('username') == PSYCHOLOGIST_USERNAME or u.get('email') == PSYCHOLOGIST_EMAIL:
                    # Güncelle
                    u['id'] = user.id
                    u['username'] = PSYCHOLOGIST_USERNAME
                    u['email'] = PSYCHOLOGIST_EMAIL
                    u['password_hash'] = user.password  # Django'nun hash'lediği şifre
                    u['role'] = 'psychologist'  # Role ekle
                    psychologist_found = True
                    break
            
            if not psychologist_found:
                # Yeni psikolog kullanıcısı ekle
                psychologist_user = {
                    'id': user.id,
                    'username': PSYCHOLOGIST_USERNAME,
                    'email': PSYCHOLOGIST_EMAIL,
                    'password_hash': user.password,  # Django'nun hash'lediği şifre
                    'role': 'psychologist',  # Role ekle
                    'created_at': None
                }
                users.append(psychologist_user)
            
            data['users'] = users
            
            with open(storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.stdout.write(self.style.SUCCESS('Psychologist user added to user_data.json'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not update user_data.json: {e}'))
        
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('PSYCHOLOGIST LOGIN CREDENTIALS:'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'Username: {PSYCHOLOGIST_USERNAME}'))
        self.stdout.write(self.style.SUCCESS(f'Email: {PSYCHOLOGIST_EMAIL}'))
        self.stdout.write(self.style.SUCCESS(f'Password: {PSYCHOLOGIST_PASSWORD}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Psychologist seeding completed!'))

