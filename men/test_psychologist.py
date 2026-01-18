"""
Test script - Psikolog kullanıcısını kontrol et ve oluştur
Bu script'i çalıştırmak için: python test_psychologist.py
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
print("PSİKOLOG KULLANICI KONTROLÜ")
print("=" * 60)

# Kullanıcıyı kontrol et
try:
    user = User.objects.get(username__iexact=PSYCHOLOGIST_USERNAME)
    print(f"✓ Kullanıcı bulundu: {user.username}")
    print(f"  - Email: {user.email}")
    print(f"  - ID: {user.id}")
    print(f"  - Active: {user.is_active}")
    
    # Şifre kontrolü
    if user.check_password(PSYCHOLOGIST_PASSWORD):
        print(f"✓ Şifre doğru!")
    else:
        print(f"✗ Şifre yanlış!")
        print(f"  Şifreyi güncelliyorum...")
        user.set_password(PSYCHOLOGIST_PASSWORD)
        user.save()
        print(f"✓ Şifre güncellendi!")
    
    # Profile kontrolü
    profile = Profile.objects.filter(user=user).first()
    if profile:
        print(f"✓ Profile bulundu")
        print(f"  - Role: {profile.role}")
        if profile.role != 'psychologist':
            print(f"  ⚠ Role 'psychologist' değil, güncelliyorum...")
            profile.role = 'psychologist'
            profile.save()
            print(f"  ✓ Role güncellendi!")
    else:
        print(f"✗ Profile bulunamadı, oluşturuluyor...")
        profile = Profile.objects.create(user=user, role='psychologist')
        print(f"✓ Profile oluşturuldu (role: psychologist)")
    
    print("")
    print("=" * 60)
    print("TEST: Manuel Authentication")
    print("=" * 60)
    
    # Manuel authentication testi
    from django.contrib.auth import authenticate
    auth_user = authenticate(username=PSYCHOLOGIST_USERNAME, password=PSYCHOLOGIST_PASSWORD)
    if auth_user:
        print(f"✓ Django authenticate başarılı!")
        print(f"  - User: {auth_user.username}")
    else:
        print(f"✗ Django authenticate başarısız!")
        print(f"  Kullanıcı adı veya şifre hatalı olabilir.")
    
except User.DoesNotExist:
    print(f"✗ Kullanıcı bulunamadı: {PSYCHOLOGIST_USERNAME}")
    print(f"  Seed komutunu çalıştırın: python manage.py seed_psychologist")
except Exception as e:
    print(f"✗ Hata: {e}")

print("")
print("=" * 60)
print("TÜM KULLANICILAR")
print("=" * 60)
all_users = User.objects.all()
for u in all_users:
    profile = Profile.objects.filter(user=u).first()
    role = profile.role if profile else "N/A"
    print(f"- {u.username} ({u.email}) - Role: {role}")

