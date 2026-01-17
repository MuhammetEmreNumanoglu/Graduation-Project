"""
Kullanıcı bilgilerini kalıcı JSON dosyasında saklayan yardımcı modül.
Bu modül, Django veritabanına ek olarak kullanıcı bilgilerini JSON dosyasına yedekler.
"""
import json
import os
from pathlib import Path
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from typing import Dict, Optional, List


# Kullanıcı verilerinin saklanacağı dosya yolu
STORAGE_FILE = Path(settings.BASE_DIR) / 'user_data.json'


def ensure_storage_file():
    """JSON dosyasının var olduğundan emin ol, yoksa oluştur."""
    if not STORAGE_FILE.exists():
        with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump({'users': []}, f, ensure_ascii=False, indent=2)


def load_users() -> Dict:
    """JSON dosyasından tüm kullanıcıları yükle."""
    ensure_storage_file()
    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'users' not in data:
                data = {'users': []}
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        return {'users': []}


def save_users(data: Dict):
    """Kullanıcı verilerini JSON dosyasına kaydet."""
    ensure_storage_file()
    with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def register_user(user_id: int, username: str, email: str, password_hash: str) -> bool:
    """
    Yeni kullanıcı kaydı yap.
    
    Args:
        user_id: Django User modelindeki kullanıcı ID'si
        username: Kullanıcı adı
        email: E-posta adresi
        password_hash: Şifrenin hash'lenmiş hali
    
    Returns:
        bool: Kayıt başarılı ise True
    """
    data = load_users()
    users = data['users']
    
    # Kullanıcı adı veya e-posta zaten varsa kaydetme
    if any(u.get('username') == username or u.get('email') == email for u in users):
        return False
    
    new_user = {
        'id': user_id,
        'username': username,
        'email': email,
        'password_hash': password_hash,
        'created_at': None  # Django tarafından yönetiliyor
    }
    
    users.append(new_user)
    data['users'] = users
    save_users(data)
    return True


def verify_user(username: str, password: str) -> Optional[Dict]:
    """
    Kullanıcı adı ve şifre ile kullanıcıyı doğrula.
    
    Args:
        username: Kullanıcı adı
        password: Düz metin şifre
    
    Returns:
        Dict: Kullanıcı bilgileri dict'i, doğrulama başarısız ise None
    """
    data = load_users()
    users = data['users']
    
    # Kullanıcı adı veya e-posta ile ara
    user = None
    for u in users:
        if u.get('username') == username or u.get('email') == username:
            user = u
            break
    
    if not user:
        return None
    
    # Şifreyi kontrol et
    password_hash = user.get('password_hash')
    if password_hash and check_password(password, password_hash):
        # Şifre hash'ini return etme
        return {
            'id': user.get('id'),
            'username': user.get('username'),
            'email': user.get('email')
        }
    
    return None


def get_user_by_username(username: str) -> Optional[Dict]:
    """Kullanıcı adı veya e-posta ile kullanıcı bilgilerini getir."""
    data = load_users()
    users = data['users']
    
    for u in users:
        if u.get('username') == username or u.get('email') == username:
            return {
                'id': u.get('id'),
                'username': u.get('username'),
                'email': u.get('email')
            }
    
    return None


def update_user(user_id: int, **kwargs) -> bool:
    """
    Kullanıcı bilgilerini güncelle.
    
    Args:
        user_id: Kullanıcı ID'si
        **kwargs: Güncellenecek alanlar (username, email, password_hash)
    
    Returns:
        bool: Güncelleme başarılı ise True
    """
    data = load_users()
    users = data['users']
    
    for u in users:
        if u.get('id') == user_id:
            for key, value in kwargs.items():
                if key in u:
                    u[key] = value
            save_users(data)
            return True
    
    return False


def delete_user(user_id: int) -> bool:
    """Kullanıcıyı JSON dosyasından sil."""
    data = load_users()
    users = data['users']
    
    original_count = len(users)
    data['users'] = [u for u in users if u.get('id') != user_id]
    
    if len(data['users']) < original_count:
        save_users(data)
        return True
    
    return False


def get_all_users() -> List[Dict]:
    """Tüm kullanıcıların listesini döndür (şifre hash'leri hariç)."""
    data = load_users()
    users = data['users']
    
    return [
        {
            'id': u.get('id'),
            'username': u.get('username'),
            'email': u.get('email')
        }
        for u in users
    ]

