from django.shortcuts import render, HttpResponse, redirect
from .forms import CreateUserForm, LoginForm, ArticleForm, UpdateUserForm,UpdateProfileForm, EmergencyContactForm
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import StreamingHttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
# ai_wrapper import'u artık ai_services içinde kullanıldığı için burada gerekmeyebilir, ama zararı yok.
from .ai_wrapper import LLMClient 
# YENİ: Gelişmiş AI servislerimizi ve yeni modellerimizi import ediyoruz
from .ai_services import call_ai_model, get_updated_memory_json
from .models import Article, Profile, DailyMood, ChatHistory, ChatHistoryContent, Like, EmergencyContact, UserAIAssistantProfile, Task, Notification, PsychologistMessage, LoginActivity, PsychologistUserRelation, SessionRating, ForumPost, ForumComment, ForumLike
from django.http import JsonResponse
from django.utils import translation, timezone
from django.conf import settings
from django.urls import reverse
from django.utils.translation import get_language, gettext as _
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import json
import uuid
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
# YENİ: Kullanıcı verilerini JSON dosyasına yedeklemek için
from .user_storage import register_user as storage_register_user


# Create your views here.


def homepage(request):
    return render(request, "articles/index.html")


def register(request):
    form = CreateUserForm(request.POST or None)
    if form.is_valid():
        current_user = form.save(commit=False)
        form.save()
        # Profile oluştururken role='member' olarak ayarla
        profile = Profile.objects.create(user=current_user, role='member')
        # YENİ: Yeni kullanıcı için AI profilini de oluşturuyoruz
        UserAIAssistantProfile.objects.create(user=current_user)
        
        messages.success(request, _("Kullanıcı Oluşturuldu!"))
        return redirect("my-login")
    context = {"RegistrationForm": form}
    return render(request, "articles/register.html", context)


def my_login(request):
    """
    Üye giriş sayfası - Sadece member rolündeki kullanıcılar giriş yapabilir.
    """
    form = LoginForm()
    
    if request.method == "POST":
        # Django AuthenticationForm kullan
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            # Django form zaten authenticate ediyor, user'ı al
            user = form.get_user()
            
            # Profile'ı kontrol et veya oluştur
            profile = Profile.objects.filter(user=user).first()
            if not profile:
                profile = Profile.objects.create(user=user, role='member')
            
            # Psikolog hesabı üye girişinde kullanılamaz
            if profile.role == 'psychologist':
                messages.error(request, _("Bu hesap psikolog hesabıdır. Lütfen psikolog giriş sayfasını kullanın."))
                form = LoginForm()  # Formu temizle
            else:
                # Normal üye girişi - dashboard'a yönlendir
                if profile.role != 'member':
                    profile.role = 'member'
                    profile.save()
                
                auth.login(request, user)
                
                # LoginActivity kaydı - aktif günler için
                from datetime import date
                LoginActivity.objects.get_or_create(user=user, login_date=date.today())
                
                remember_me = form.cleaned_data.get('remember_me', False)
                
                if remember_me:
                    request.session.set_expiry(30 * 24 * 60 * 60)  # 30 gün
                else:
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                
                return redirect("dashboard")
        else:
            # Form hataları - Django AuthenticationForm hatalarını göster
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        messages.error(request, f"{field}: {error}")
    
    context = {"LoginForm": form}
    return render(request, "articles/my-login.html", context)


def psychologist_login(request):
    """
    Psikolog giriş sayfası - Sadece psychologist rolündeki kullanıcılar giriş yapabilir.
    """
    form = LoginForm()
    
    if request.method == "POST":
        # Form verilerini al
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Kullanıcıyı kontrol et - önce username ile, sonra email ile
        user = None
        try:
            # Önce username ile dene (case-insensitive)
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            try:
                # Sonra email ile dene (case-insensitive)
                user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                pass
        
        if user:
            # Kullanıcı bulundu, şifreyi kontrol et
            if user.check_password(password):
                # Şifre doğru, profile'ı kontrol et
                profile = Profile.objects.filter(user=user).first()
                
                if not profile:
                    # Profile yoksa oluştur (ama bu durumda psikolog olmaz)
                    messages.error(request, _("Bu hesap psikolog hesabı değil."))
                    form = LoginForm()
                elif profile.role != 'psychologist':
                    # Role 'psychologist' değilse
                    messages.error(request, _("Bu hesap psikolog hesabı değil. Bilgiler hatalı."))
                    form = LoginForm()
                else:
                    # Her şey doğru, giriş yap
                    auth.login(request, user)
                    remember_me = request.POST.get('remember_me', False)
                    
                    if remember_me:
                        request.session.set_expiry(30 * 24 * 60 * 60)  # 30 gün
                    else:
                        request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                    
                    return redirect("psychologist-dashboard")
            else:
                # Şifre yanlış
                messages.error(request, _("Kullanıcı adı veya şifre hatalı."))
                form = LoginForm()
        else:
            # Kullanıcı bulunamadı - eğer "kristin" ise otomatik oluştur
            if username.lower() == 'kristin' and password == '123456789aB':
                # Psikolog kullanıcısını otomatik oluştur
                try:
                    user = User.objects.create_user(
                        username='kristin',
                        email='kristin@gmail.com',
                        password='123456789aB'
                    )
                    user.is_active = True
                    user.save()
                    
                    # Profile oluştur
                    profile = Profile.objects.create(user=user, role='psychologist')
                    
                    # Giriş yap
                    auth.login(request, user)
                    remember_me = request.POST.get('remember_me', False)
                    
                    if remember_me:
                        request.session.set_expiry(30 * 24 * 60 * 60)  # 30 gün
                    else:
                        request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                    
                    messages.success(request, _("Psikolog hesabı oluşturuldu ve giriş yapıldı."))
                    return redirect("psychologist-dashboard")
                except Exception as e:
                    messages.error(request, _("Kullanıcı oluşturulurken bir hata oluştu. Lütfen 'python manage.py seed_psychologist' komutunu çalıştırın."))
                    form = LoginForm()
            else:
                messages.error(request, _("Kullanıcı adı veya şifre hatalı."))
                form = LoginForm()
    
    context = {"LoginForm": form}
    return render(request, "articles/my-login-2.html", context)


# ==========================================================
# === DECORATORS - Role Based Access Control ===
# ==========================================================

def member_required(view_func):
    """Üye kontrolü yapan decorator - DB'den role kontrolü"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('my-login')
        
        # Profile'dan role kontrolü
        try:
            profile = Profile.objects.get(user=request.user)
            if profile.role != 'member':
                # Psikolog ise psychologist-dashboard'a sessizce yönlendir (hata mesajı gösterme)
                if profile.role == 'psychologist':
                    return redirect('psychologist-dashboard')
                # Diğer roller için sessizce login'e yönlendir
                return redirect('my-login')
        except Profile.DoesNotExist:
            # Profile yoksa member olarak oluştur
            profile = Profile.objects.create(user=request.user, role='member')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def psychologist_required(view_func):
    """Psikolog kontrolü yapan decorator - DB'den role kontrolü"""
    from functools import wraps
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # AJAX mi yoksa normal sayfa isteği mi?
        is_ajax = (
            request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            or 'application/json' in request.headers.get('Accept', '')
            or request.content_type == 'application/json'
        )

        if not request.user.is_authenticated:
            if is_ajax:
                return JsonResponse({'success': False, 'error': 'Kimlik doğrulaması gerekli.'}, status=401, content_type='application/json')
            return redirect('psychologist-login')

        # Profile'dan role kontrolü
        try:
            profile = Profile.objects.get(user=request.user)
            if profile.role != 'psychologist':
                if is_ajax:
                    return JsonResponse({'success': False, 'error': 'Bu işlem için psikolog yetkisi gerekli.'}, status=403, content_type='application/json')
                messages.error(request, _("Bu sayfaya erişim için psikolog hesabı gereklidir."))
                return redirect('psychologist-login')
        except Profile.DoesNotExist:
            if is_ajax:
                return JsonResponse({'success': False, 'error': 'Profil bulunamadı.'}, status=403, content_type='application/json')
            messages.error(request, _("Profil bulunamadı. Lütfen tekrar giriş yapın."))
            return redirect('psychologist-login')

        return view_func(request, *args, **kwargs)
    return wrapper


@member_required
def dashboard(request):
    """Üye dashboard sayfası - Sadece member role erişebilir"""
    profile_pic = Profile.objects.filter(user=request.user).first()
    if not profile_pic:
        profile_pic = Profile.objects.create(user=request.user)
    context = {'profilePic': profile_pic}
    return render(request, "articles/dashboard.html", context)

# =========================================================================================
# === GELİŞMİŞ AI SOHBET FONKSİYONU BURADA ===
# =========================================================================================
@login_required(login_url="my-login")
def stream_llm_response(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Only POST allowed.")

    # 1. Mevcut Veritabanı Mantığınızı Koruyoruz
    data = json.loads(request.body)
    message = data.get("message")
    history_id = data.get("history_id")

    if not history_id:
        history_id = str(uuid.uuid4())
        chat_history_db = ChatHistory.objects.create(
            user=request.user,
            history_id=history_id,
            title=message[:40]
        )
    else:
        chat_history_db = ChatHistory.objects.filter(history_id=history_id, user=request.user).first()
        if not chat_history_db:
            return JsonResponse({"error": _("Geçersiz history_id")}, status=400)

    ChatHistoryContent.objects.create(
        chat_history=chat_history_db,
        role="user",
        content=message
    )

    # 2. Uzun Süreli Hafızayı Çekiyoruz
    profile, created = UserAIAssistantProfile.objects.get_or_create(user=request.user)
    if created or not profile.long_term_memory:
        try:
            with open('long_term_memory_template.json', 'r', encoding='utf-8') as f:
                profile.long_term_memory = json.load(f)
            profile.save()
        except FileNotFoundError:
            profile.long_term_memory = { "userID": request.user.id, "userProfile": {}, "longTermMemory": {}, "sessionHistorySummary": [] }
            profile.save()

    memory_json = profile.long_term_memory

    # 3. Gelişmiş AI Servisimizi Çağırıyoruz
    session_history_queryset = ChatHistoryContent.objects.filter(chat_history=chat_history_db).order_by('created_at')
    session_history_list = [f"{'Kullanıcı' if msg.role == 'user' else 'AI'}: {msg.content}" for msg in session_history_queryset]
    
    ai_response_json = call_ai_model(
        memory_json=memory_json,
        chat_history=session_history_list,
        new_message=message
    )
    
    # 4. Cevabı Veritabanına ve Frontend'e İletiyoruz
    response_content = ai_response_json.get('reply_text', 'Bir hata oluştu.')
    ChatHistoryContent.objects.create(
        chat_history=chat_history_db,
        role="assistant",
        content=response_content
    )
    ai_response_json['history_id'] = history_id
    
    return JsonResponse(ai_response_json)

# =========================================================================================
# === DİĞER TÜM FONKSİYONLARINIZ BURADA KORUNUYOR ===
# =========================================================================================

def user_logout(request):
    auth.logout(request)
    request.session.flush()
    return redirect("my-login")


@login_required(login_url="my-login")
def create_article(request):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect("dashboard")
    context = {"CreateArticleForm": form}
    return render(request, "articles/create-article.html", context)


@login_required(login_url="my-login")
def my_articles(request):
    current_user = request.user.id
    articles = Article.objects.all().filter(user=current_user)
    context = {"AllArticles": articles}
    return render(request, "articles/my-articles.html", context)


# ... [Sizin diğer tüm fonksiyonlarınız (update_articles, delete_articles, profile_management vb.) burada devam ediyor] ...
# ... [Bu fonksiyonları buraya geri ekledim, bu yüzden dosyanın geri kalanını önceki halinden alabilirsiniz] ...
# KODUNUZUN GERİ KALANINI BURAYA EKLEYİN
# (update_articles, delete_articles, profile_management, vb. fonksiyonların tamamı)

@login_required(login_url="my-login")
def update_articles(request, pk):
    try:
        article = Article.objects.get(id=pk, user=request.user)

    except:
        return redirect("my-articles")

    form = ArticleForm(instance=article)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect("my-articles")
    context = {"UpdateArticleForm": form}
    return render(request, "articles/update-article.html", context)


@login_required(login_url="my-login")
def delete_articles(request, pk):
    try:
        article = Article.objects.get(id=pk, user=request.user)

    except:
        return redirect("my-articles")
    if request.method == "POST":
        article.delete()
        return redirect("my-articles")

    return render(request, "articles/delete-article.html")


@login_required(login_url="my-login")
def profile_management(request):
    # DB'den role kontrolü
    profile = Profile.objects.filter(user=request.user).first()
    
    if not profile:
        # Profile yoksa member olarak oluştur
        profile = Profile.objects.create(user=request.user, role='member')
    
    if profile.role == 'psychologist':
        # Psikolog için özel context - DB'den bilgileri al
        form = UpdateUserForm(instance=request.user)
        form_2 = UpdateProfileForm(instance=profile)
        
        if request.method == "POST":
            # Psikolog için sadece user info ve profile pic güncellemesi
            if 'profile_pic' in request.FILES or 'profile_pic-clear' in request.POST:
                # Profile pic güncelleme
                form_2 = UpdateProfileForm(request.POST, request.FILES, instance=profile)
                if form_2.is_valid():
                    form_2.save()
                    messages.success(request, _("Profil fotoğrafı güncellendi."))
                    return redirect("psychologist-dashboard")
            else:
                # User info güncelleme
                form = UpdateUserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, _("Bilgiler güncellendi."))
                return redirect("psychologist-dashboard")
        
        context = {
            'is_psychologist': True,
            'psychologist_email': request.user.email,
            'psychologist_username': request.user.username,
            'psychologist_profile': profile,
            'UserUpdateForm': form,
            'ProfileUpdateForm': form_2
        }
        return render(request, "articles/profile-management.html", context)
    
    # Normal üye için mevcut kod
    form = UpdateUserForm(instance=request.user)
    profile = Profile.objects.filter(user=request.user).first()
    form_2 = UpdateProfileForm(instance=profile)
    # Emergency contacts
    contact = EmergencyContact.objects.filter(user=request.user).first()
    contact_form = EmergencyContactForm(instance=contact)
    if request.method == "POST":
        # Hayat Hikayem güncellemesi (uzun metin)
        if 'life_story' in request.POST:
            profile.life_story = (request.POST.get('life_story') or '').strip()
            profile.save(update_fields=['life_story'])
            messages.success(request, _("Hayat hikayeniz kaydedildi."))
            return redirect("profile-management")
        # Detect which form is sent by checking known fields
        if 'relation' in request.POST and 'full_name' in request.POST and 'phone' in request.POST:
            contact = EmergencyContact.objects.filter(user=request.user).first()
            contact_form = EmergencyContactForm(request.POST, instance=contact)
            if contact_form.is_valid():
                obj = contact_form.save(commit=False)
                obj.user = request.user
                obj.save()
                messages.success(request, _("Acil durum kişisi kaydedildi."))
                return redirect("profile-management")
        else:
            form = UpdateUserForm(request.POST, instance=request.user)
            form_2 = UpdateProfileForm(request.POST, request.FILES, instance=profile)

            if form.is_valid():
                form.save()
                return redirect("dashboard")
            if form_2.is_valid():
                form_2.save()
                return redirect("dashboard")

    context = {"UserUpdateForm": form, 'ProfileUpdateForm': form_2, 'EmergencyContactForm': contact_form, 'contact': contact, 'is_psychologist': False}
    return render(request, "articles/profile-management.html", context)


@require_GET
@login_required(login_url="my-login")
def get_today_mood(request):
    """Üye için bugünkü ruh hali var mı?"""
    from datetime import date
    today = date.today()
    obj = DailyMood.objects.filter(user=request.user, date=today).first()
    if not obj:
        return JsonResponse({"success": True, "has_mood": False}, content_type='application/json')
    return JsonResponse({
        "success": True,
        "has_mood": True,
        "date": obj.date.isoformat(),
        "mood": obj.mood,
        "mood_label": obj.get_mood_display(),
        "note": obj.note or ""
    }, content_type='application/json')


@require_POST
@login_required(login_url="my-login")
def submit_today_mood(request):
    """Üye için günde 1 kez ruh hali kaydı."""
    from datetime import date
    mood = (request.POST.get('mood') or '').strip()
    note = (request.POST.get('note') or '').strip()

    valid_moods = {k for (k, _) in DailyMood.MOOD_CHOICES}
    if mood not in valid_moods:
        return JsonResponse({"success": False, "error": _("Geçersiz ruh hali seçimi.")}, status=400, content_type='application/json')

    today = date.today()
    obj = DailyMood.objects.filter(user=request.user, date=today).first()
    if obj:
        return JsonResponse({"success": False, "error": _("Bugünkü ruh hali zaten kaydedilmiş.")}, status=409, content_type='application/json')

    DailyMood.objects.create(
        user=request.user,
        date=today,
        mood=mood,
        note=note[:280] if note else None,
    )
    return JsonResponse({"success": True, "message": _("Ruh haliniz kaydedildi.")}, content_type='application/json')


@login_required(login_url="my-login")
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, _("Hesabınız başarıyla silindi."))
        return redirect("register")
    return render(request, "articles/delete-account.html")


@login_required(login_url="my-login")
def acil_destek(request):
    return render(request, "articles/acil-destek.html")

@login_required(login_url="my-login")
def gunluk_kartlar(request):
    return render(request, "articles/gunluk-kartlar.html")

@login_required(login_url="my-login")
def destek_duvari(request):
    """Forum / Destek Duvari - ForumPost modeli kullanir."""
    profile_pic = Profile.objects.filter(user=request.user).first()
    if not profile_pic:
        profile_pic = Profile.objects.create(user=request.user)

    page = int(request.GET.get('page', 1))
    all_posts = ForumPost.objects.all().order_by('-created_at')
    paginator = Paginator(all_posts, 5)
    posts_page = paginator.get_page(page)

    liked_post_ids = set(
        ForumLike.objects.filter(user=request.user, post__in=posts_page.object_list).values_list('post_id', flat=True)
    )

    return render(request, "articles/destek-duvari.html", {
        "posts": posts_page,
        "liked_post_ids": liked_post_ids,
        "page": page,
        "total_pages": paginator.num_pages,
        "profile_pic": profile_pic,
    })

@login_required(login_url="my-login")
def haftalik_raporlar(request):
    return render(request, "articles/haftalik-raporlar.html")

@login_required(login_url="my-login")
def bildirimler(request):
    return render(request, "articles/bildirimler.html")

@login_required(login_url="my-login")
def settings_view(request):
    return render(request, "articles/settings.html")

@login_required(login_url="my-login")
def help_center(request):
    return render(request, "articles/help-center.html")


@login_required(login_url="my-login")
def update_password(request):
    if request.method == "POST":
        try:
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            
            if not current_password or not new_password:
                messages.error(request, _('Lütfen tüm alanları doldurunuz.'))
                return redirect('profile-management')
            
            user = request.user
            if user.check_password(current_password):
                if current_password == new_password:
                    messages.error(request, _('Yeni şifre mevcut şifre ile aynı olamaz.'))
                    return redirect('profile-management')
                
                try:
                    validate_password(new_password, user)
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, _('Şifreniz başarıyla güncellendi.'))
                    return redirect('anasayfa')
                except ValidationError as e:
                    try:
                        for err in e:
                            messages.error(request, str(err))
                    except Exception:
                        messages.error(request, _('Şifre güncellenemedi.'))
                    return redirect('profile-management')
            else:
                messages.error(request, _('Mevcut şifre yanlış.'))
                return redirect('profile-management')
                
        except Exception as e:
            messages.error(request, _('Şifre güncellenemedi.'))
            return redirect('profile-management')
    return redirect('profile-management')

def contact(request):
    return render(request, "articles/contact.html")
@login_required(login_url="my-login")
def anasayfa(request):
    # Kullanıcının görevlerini ve bildirimlerini getir
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')[:10]
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:10]
    
    context = {
        'tasks': tasks,
        'notifications': notifications
    }
    return render(request, "articles/anasayfa.html", context)
@login_required(login_url="my-login")
def meditasyon(request):
    return render(request, 'articles/meditasyon.html')
@login_required(login_url="my-login")
def nefes_egzersizi(request):
    return render(request, 'articles/nefes-egzersizi.html')
@login_required(login_url="my-login")
def meditasyon_audio(request, audio_id):
    audio_map = {
        'rain': { 'title': 'Derin Uyku İçin Yağmur', 'image_url': '...', 'audio_url': '...', },
        'waves': { 'title': 'Stres Azaltan Dalgalar', 'image_url': '...', 'audio_url': '...', },
        'morning': { 'title': 'Sabah Esnemesi', 'image_url': '...', 'audio_url': '...', },
        'piano': { 'title': 'Odaklanma Piyanosu', 'image_url': '...', 'audio_url': '...', },
    }
    data = audio_map.get(audio_id)
    if not data:
        return redirect('meditasyon')
    return render(request, 'articles/meditasyon_audio.html', data)

@login_required(login_url="my-login")
def upload_photo(request):
    if request.method == "POST":
        try:
            profile = Profile.objects.get(user=request.user)
            if 'profile_photo' in request.FILES:
                profile.avatar = request.FILES['profile_photo']
                profile.save()
                return JsonResponse({'success': True, 'message': _('Profil fotoğrafı başarıyla güncellendi!')})
            else:
                return JsonResponse({'success': False, 'error': _('Fotoğraf dosyası bulunamadı.')}, status=400)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)
            if 'profile_photo' in request.FILES:
                profile.avatar = request.FILES['profile_photo']
                profile.save()
                return JsonResponse({'success': True, 'message': _('Profil fotoğrafı başarıyla güncellendi!')})
            else:
                return JsonResponse({'success': False, 'error': _('Fotoğraf dosyası bulunamadı.')}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': _('Bir hata oluştu: ') + str(e)}, status=500)
    return JsonResponse({'success': False, 'error': _('Sadece POST istekleri kabul edilir.')}, status=405)

def responsive(request):
    return render(request, 'articles/responsive.html')

@require_GET
def check_availability(request):
    """Username ve email için anlık DB kontrolü - JSON döner"""
    field = request.GET.get('field')
    value = request.GET.get('value', '').strip()
    current_user_id = None
    if request.user.is_authenticated:
        current_user_id = request.user.id
    if not field or not value:
        return JsonResponse({'available': False, 'error': _('Geçersiz istek')}, status=400, content_type='application/json')
    if field == 'username':
        qs = User.objects.filter(username__iexact=value)
        if current_user_id:
            qs = qs.exclude(pk=current_user_id)
        return JsonResponse({'available': not qs.exists()}, content_type='application/json')
    elif field == 'email':
        qs = User.objects.filter(email__iexact=value)
        if current_user_id:
            qs = qs.exclude(pk=current_user_id)
        return JsonResponse({'available': not qs.exists()}, content_type='application/json')
    else:
        return JsonResponse({'available': False, 'error': _('Bilinmeyen alan')}, status=400, content_type='application/json')

@require_POST
@login_required(login_url="my-login")
def like_story(request):
    story_id = request.POST.get("story_id")
    try:
        story = ChatHistoryContent.objects.get(id=story_id)
        like, created = Like.objects.get_or_create(user=request.user, story=story)
        if not created:
            like.delete()
            story.likes = Like.objects.filter(story=story).count()
            story.save()
            return JsonResponse({"success": True, "likes": story.likes, "liked": False})
        else:
            story.likes = Like.objects.filter(story=story).count()
            story.save()
            return JsonResponse({"success": True, "likes": story.likes, "liked": True})
    except ChatHistoryContent.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Mesaj bulunamadı.")}, status=404)


# ==========================================================
# === PSİKOLOG SİSTEMİ VIEW'LARI ===
# ==========================================================

@psychologist_required
def psychologist_dashboard(request):
    """Psikolog dashboard sayfası - Tüm üyeleri listele (psikolog hariç)"""
    # Psikolog profil bilgilerini al
    psychologist_profile = Profile.objects.filter(user=request.user).first()
    if not psychologist_profile:
        psychologist_profile = Profile.objects.create(user=request.user)
    
    # Sadece member role'lü kullanıcıları al (psikolog kendi kartını ve admin'leri görmesin)
    member_profiles = Profile.objects.filter(role='member')
    member_users = [profile.user for profile in member_profiles]
    
    # Psikologun kendi ID'sini ve admin/superuser'ları filtrele
    member_users = [user for user in member_users if user.id != request.user.id and not user.is_staff and not user.is_superuser]
    
    # Her kullanıcı için son mesaj zamanını ve kategoriyi hesapla
    users_with_last_message = []
    for user in member_users:
        last_message = PsychologistMessage.objects.filter(user=user).order_by('-created_at').first()
        # Psikolog-kullanıcı ilişkisini al veya oluştur (category/notes için)
        relation, _ = PsychologistUserRelation.objects.get_or_create(
            psychologist=request.user,
            user=user,
            defaults={'category': 'normal'}
        )
        users_with_last_message.append({
            'user': user,
            'last_message_time': last_message.created_at if last_message else None,
            'category': relation.category,
        })
    
    # Son mesaj zamanına göre sırala (en yeni üstte)
    users_with_last_message.sort(key=lambda x: x['last_message_time'] if x['last_message_time'] else x['user'].date_joined, reverse=True)
    
    context = {
        'users': users_with_last_message,
        'psychologist_profile': psychologist_profile
    }
    return render(request, "articles/psychologist-dashboard.html", context)


@psychologist_required
def psychologist_chat(request, user_id):
    """Psikolog'un belirli bir üye ile sohbet sayfası"""
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('psychologist-dashboard')
    
    messages = PsychologistMessage.objects.filter(user=target_user).order_by('created_at')

    # Sağ bilgi paneli verileri
    from datetime import date, timedelta
    today = date.today()
    today_mood = DailyMood.objects.filter(user=target_user, date=today).first()
    recent_moods = list(
        DailyMood.objects.filter(user=target_user, date__gte=today - timedelta(days=7))
        .order_by('-date')[:7]
    )
    target_profile = Profile.objects.filter(user=target_user).first()
    life_story = (target_profile.life_story if target_profile else "") or ""
    
    context = {
        'target_user': target_user,
        'messages': messages,
        'today_mood': today_mood,
        'recent_moods': recent_moods,
        'life_story': life_story,
    }
    return render(request, "articles/psychologist-chat.html", context)


@require_GET
@psychologist_required
def get_user_insights(request):
    """Psikolog dashboard chat için: seçilen kullanıcıya ait ruh hali + hayat hikayesi."""
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({
            "success": False,
            "error": _("Kullanıcı ID gerekli.")
        }, status=400, content_type='application/json')

    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": _("Kullanıcı bulunamadı.")
        }, status=404, content_type='application/json')

    # Profil opsiyonel; rol kısıtlaması kaldırıldı ki eski/veri hatalı hesaplarda da çalışsın
    try:
        profile = Profile.objects.get(user=target_user)
    except Profile.DoesNotExist:
        profile = None

    from datetime import date, timedelta
    today = date.today()
    today_mood = DailyMood.objects.filter(user=target_user, date=today).first()
    recent_moods_data = []
    for i in range(3):
        d = today - timedelta(days=i)
        mood_obj = DailyMood.objects.filter(user=target_user, date=d).first()
        if mood_obj:
            recent_moods_data.append({
                "date": d.isoformat(),
                "mood": mood_obj.mood,
                "mood_label": mood_obj.get_mood_display(),
                "note": mood_obj.note or "",
            })
        else:
            recent_moods_data.append({
                "date": d.isoformat(),
                "mood": None,
                "mood_label": _("Kayıt yok"),
                "note": "",
            })

    data = {
        "success": True,
        "today_mood": None,
        "recent_moods": recent_moods_data,
        "life_story": (profile.life_story if profile else "") or "",
    }

    if today_mood:
        data["today_mood"] = {
            "date": today_mood.date.isoformat(),
            "mood": today_mood.mood,
            "mood_label": today_mood.get_mood_display(),
            "note": today_mood.note or "",
        }

    return JsonResponse(data, content_type='application/json')


@require_POST
@psychologist_required
def send_task(request):
    """Psikolog'un üyeye görev göndermesi"""
    user_id = request.POST.get('user_id')
    text = request.POST.get('text')
    
    if not user_id or not text:
        return JsonResponse({"success": False, "error": _("Kullanıcı ID ve görev metni gerekli.")}, status=400)
    
    try:
        user = User.objects.get(id=user_id)
        
        # Admin/superuser kontrolü
        if user.is_staff or user.is_superuser:
            return JsonResponse({"success": False, "error": _("Admin kullanıcılarına görev gönderilemez.")}, status=403)
        
        # Role kontrolü
        try:
            profile = Profile.objects.get(user=user)
            if profile.role != 'member':
                return JsonResponse({"success": False, "error": _("Sadece üyelere görev gönderilebilir.")}, status=403)
        except Profile.DoesNotExist:
            return JsonResponse({"success": False, "error": _("Kullanıcı profili bulunamadı.")}, status=404)
        
        task = Task.objects.create(user=user, text=text)
        
        # Otomatik bildirim oluştur
        task_names = {
            'support_wall': _('Destek Duvarı'),
            'daily_cards': _('Günlük Kartlar'),
            'meditation': _('Meditasyon'),
            'breathing_exercise': _('Nefes Egzersizi')
        }
        display_name = task_names.get(text, text)
        notification_text = _('Sana yeni bir görev atandı: {}').format(display_name)
        Notification.objects.create(user=user, text=notification_text)
        
        return JsonResponse({"success": True, "task_id": task.id, "message": _("Görev başarıyla gönderildi.")}, content_type='application/json')
    except User.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Kullanıcı bulunamadı.")}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_POST
@psychologist_required
def send_notification(request):
    """Psikolog'un üyeye bildirim göndermesi"""
    user_id = request.POST.get('user_id')
    text = request.POST.get('text')
    
    if not user_id or not text:
        return JsonResponse({"success": False, "error": _("Kullanıcı ID ve bildirim metni gerekli.")}, status=400)
    
    try:
        user = User.objects.get(id=user_id)
        
        # Admin/superuser kontrolü
        if user.is_staff or user.is_superuser:
            return JsonResponse({"success": False, "error": _("Admin kullanıcılarına bildirim gönderilemez.")}, status=403)
        
        # Role kontrolü
        try:
            profile = Profile.objects.get(user=user)
            if profile.role != 'member':
                return JsonResponse({"success": False, "error": _("Sadece üyelere bildirim gönderilebilir.")}, status=403)
        except Profile.DoesNotExist:
            return JsonResponse({"success": False, "error": _("Kullanıcı profili bulunamadı.")}, status=404)
        
        notification = Notification.objects.create(user=user, text=text)
        return JsonResponse({"success": True, "notification_id": notification.id, "message": _("Bildirim başarıyla gönderildi.")})
    except User.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Kullanıcı bulunamadı.")}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_POST
@psychologist_required
def send_psychologist_message(request):
    """Psikolog'un üyeye mesaj göndermesi"""
    try:
        user_id = request.POST.get('user_id')
        text = request.POST.get('text', '').strip()
        
        if not user_id or not text:
            return JsonResponse({
                "success": False, 
                "error": _("Kullanıcı ID ve mesaj metni gerekli.")
            }, status=400, content_type='application/json')
        
        user = User.objects.get(id=user_id)
        
        # Admin/superuser kontrolü
        if user.is_staff or user.is_superuser:
            return JsonResponse({
                "success": False,
                "error": _("Admin kullanıcılarına mesaj gönderilemez.")
            }, status=403, content_type='application/json')
        
        # Role kontrolü
        try:
            profile = Profile.objects.get(user=user)
            if profile.role != 'member':
                return JsonResponse({
                    "success": False,
                    "error": _("Sadece üyelere mesaj gönderilebilir.")
                }, status=403, content_type='application/json')
        except Profile.DoesNotExist:
            return JsonResponse({
                "success": False,
                "error": _("Kullanıcı profili bulunamadı.")
            }, status=404, content_type='application/json')
        
        message = PsychologistMessage.objects.create(
            user=user,
            sender='psychologist',
            text=text
        )
        return JsonResponse({
            "success": True,
            "message_id": message.id,
            "created_at": timezone.localtime(message.created_at).strftime("%d.%m.%Y %H:%M"),
            "message": _("Mesaj başarıyla gönderildi.")
        }, content_type='application/json')
    except User.DoesNotExist:
        return JsonResponse({
            "success": False, 
            "error": _("Kullanıcı bulunamadı.")
        }, status=404, content_type='application/json')
    except Exception as e:
        return JsonResponse({
            "success": False, 
            "error": str(e)
        }, status=500, content_type='application/json')


@require_POST
@login_required(login_url="my-login")
def send_user_message(request):
    """Üyenin psikologa mesaj göndermesi"""
    text = request.POST.get('text')
    
    if not text:
        return JsonResponse({"success": False, "error": _("Mesaj metni gerekli.")}, status=400)
    
    # Psikologa mesaj göndermek için user=request.user, sender='user' kullanılır
    message = PsychologistMessage.objects.create(
        user=request.user,
        sender='user',
        text=text
    )
    return JsonResponse({
        "success": True,
        "message_id": message.id,
        "created_at": timezone.localtime(message.created_at).strftime("%Y-%m-%d %H:%M:%S"),
        "message": _("Mesaj başarıyla gönderildi.")
    })


@login_required(login_url="my-login")
def get_psychologist_messages(request):
    """Üyenin psikolog ile mesajlarını getir - since parametresi ile incremental fetch"""
    try:
        since_id = request.GET.get('since')  # Son mesaj ID'si veya timestamp
        messages_query = PsychologistMessage.objects.filter(user=request.user)
        
        # since parametresi varsa sadece yeni mesajları getir
        if since_id:
            try:
                since_id_int = int(since_id)
                messages_query = messages_query.filter(id__gt=since_id_int)
            except ValueError:
                pass  # Invalid since, tüm mesajları getir
        
        messages = messages_query.order_by('created_at')
        messages_data = [{
            'id': msg.id,
            'sender': msg.sender,
            'text': msg.text,
            'created_at': timezone.localtime(msg.created_at).strftime("%Y-%m-%d %H:%M:%S"),
            'is_read': msg.is_read
        } for msg in messages]
        return JsonResponse({"success": True, "messages": messages_data}, content_type='application/json')
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500, content_type='application/json')


@psychologist_required
def get_user_messages(request):
    """Psikolog'un belirli bir kullanıcının mesajlarını getir - since parametresi ile incremental fetch"""
    try:
        user_id = request.GET.get('user_id')
        since_id = request.GET.get('since')  # Son mesaj ID'si
        
        if not user_id:
            return JsonResponse({
                "success": False, 
                "error": _("Kullanıcı ID gerekli.")
            }, status=400, content_type='application/json')
        
        target_user = User.objects.get(id=user_id)
        
        # Admin/superuser kontrolü
        if target_user.is_staff or target_user.is_superuser:
            return JsonResponse({
                "success": False,
                "error": _("Admin kullanıcılarına erişilemez.")
            }, status=403, content_type='application/json')
        
        # Role kontrolü
        try:
            profile = Profile.objects.get(user=target_user)
            if profile.role != 'member':
                return JsonResponse({
                    "success": False,
                    "error": _("Sadece üyelerin mesajları görüntülenebilir.")
                }, status=403, content_type='application/json')
        except Profile.DoesNotExist:
            return JsonResponse({
                "success": False,
                "error": _("Kullanıcı profili bulunamadı.")
            }, status=404, content_type='application/json')
        
        messages_query = PsychologistMessage.objects.filter(user=target_user)
        
        # since parametresi varsa sadece yeni mesajları getir
        if since_id:
            try:
                since_id_int = int(since_id)
                messages_query = messages_query.filter(id__gt=since_id_int)
            except ValueError:
                pass  # Invalid since, tüm mesajları getir
        
        messages = messages_query.order_by('created_at')
        messages_data = [{
            'id': msg.id,
            'sender': msg.sender,
            'text': msg.text,
            'created_at': timezone.localtime(msg.created_at).strftime("%d.%m.%Y %H:%M"),
            'is_read': msg.is_read
        } for msg in messages]
        return JsonResponse({
            "success": True, 
            "messages": messages_data
        }, content_type='application/json')
    except User.DoesNotExist:
        return JsonResponse({
            "success": False, 
            "error": _("Kullanıcı bulunamadı.")
        }, status=404, content_type='application/json')
    except Exception as e:
        return JsonResponse({
            "success": False, 
            "error": str(e)
        }, status=500, content_type='application/json')


@login_required(login_url="my-login")
def get_user_tasks(request):
    """Üyenin görevlerini getir"""
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    tasks_data = [{
        'id': task.id,
        'text': task.text,
        'created_at': timezone.localtime(task.created_at).strftime("%Y-%m-%d %H:%M:%S"),
        'is_completed': task.is_completed
    } for task in tasks]
    return JsonResponse({"success": True, "tasks": tasks_data})


@login_required(login_url="my-login")
def get_user_notifications(request):
    """Üyenin bildirimlerini getir"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    notifications_data = [{
        'id': notif.id,
        'text': notif.text,
        'created_at': timezone.localtime(notif.created_at).strftime("%Y-%m-%d %H:%M:%S"),
        'is_read': notif.is_read
    } for notif in notifications]
    return JsonResponse({"success": True, "notifications": notifications_data}, content_type='application/json')


@psychologist_required
def get_unread_counts(request):
    """Psikolog için her kullanıcının okunmamış mesaj sayılarını getir"""
    try:
        counts = {}
        member_profiles = Profile.objects.filter(role='member')
        for profile in member_profiles:
            user = profile.user
            # Psikolog için: sender='user' olan okunmamış mesajlar
            unread_count = PsychologistMessage.objects.filter(
                user=user,
                sender='user',
                is_read=False
            ).count()
            counts[user.id] = unread_count
        
        return JsonResponse({"success": True, "counts": counts}, content_type='application/json')
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500, content_type='application/json')


@login_required(login_url="my-login")
def get_unread_message_count(request):
    """Üye için psikologdan gelen okunmamış mesaj sayısını getir"""
    try:
        # Üye için: sender='psychologist' olan okunmamış mesajlar
        unread_count = PsychologistMessage.objects.filter(
            user=request.user,
            sender='psychologist',
            is_read=False
        ).count()
        
        return JsonResponse({"success": True, "count": unread_count}, content_type='application/json')
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500, content_type='application/json')


@login_required(login_url="my-login")
def get_member_badges(request):
    """Üye için tüm okunmamış sayıları getir (bildirimler + mesajlar + görevler)"""
    try:
        # Okunmamış bildirimler
        unread_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        
        # Okunmamış mesajlar (psikologdan gelen)
        unread_messages = PsychologistMessage.objects.filter(
            user=request.user,
            sender='psychologist',
            is_read=False
        ).count()
        
        # Okunmamış görevler (is_completed=False olanlar)
        unread_tasks = Task.objects.filter(
            user=request.user,
            is_completed=False
        ).count()
        
        # Toplam badge sayısı (Bildirimler + Mesajlar)
        total_badge = unread_notifications + unread_messages
        
        return JsonResponse({
            "success": True,
            "unread_notifications": unread_notifications,
            "unread_messages": unread_messages,
            "unread_tasks": unread_tasks,
            "total": total_badge
        }, content_type='application/json')
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500, content_type='application/json')


@require_POST
@login_required(login_url="my-login")
def mark_notifications_read(request):
    """Üye için tüm bildirimleri okundu olarak işaretle"""
    try:
        updated = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        
        return JsonResponse({
            "success": True,
            "updated_count": updated
        }, content_type='application/json')
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500, content_type='application/json')


@require_POST
@login_required(login_url="my-login")
def delete_notification(request):
    """Üye için belirli bir bildirimi sil"""
    try:
        import json
        data = json.loads(request.body)
        notif_id = data.get("notification_id")
        if not notif_id:
            return JsonResponse({"success": False, "error": _("Bildirim ID gerekli.")}, status=400)
            
        Notification.objects.filter(id=notif_id, user=request.user).delete()
        return JsonResponse({"success": True, "message": _("Bildirim başarıyla silindi.")})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@require_POST
@psychologist_required
def mark_messages_read(request):
    """Psikolog için belirli bir kullanıcının mesajlarını okundu olarak işaretle"""
    try:
        user_id = request.POST.get('user_id')
        
        if not user_id:
            return JsonResponse({
                "success": False,
                "error": _("Kullanıcı ID gerekli.")
            }, status=400, content_type='application/json')
        
        target_user = User.objects.get(id=user_id)
        # Psikolog açtığı için: sender='user' olan mesajları okundu işaretle
        updated = PsychologistMessage.objects.filter(
            user=target_user,
            sender='user',
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        
        return JsonResponse({
            "success": True,
            "updated_count": updated
        }, content_type='application/json')
    except User.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": _("Kullanıcı bulunamadı.")
        }, status=404, content_type='application/json')
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500, content_type='application/json')


@require_POST
@login_required(login_url="my-login")
def mark_psychologist_messages_read(request):
    """Üye için psikologdan gelen mesajları okundu olarak işaretle"""
    try:
        # Üye açtığı için: sender='psychologist' olan mesajları okundu işaretle
        updated = PsychologistMessage.objects.filter(
            user=request.user,
            sender='psychologist',
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        
        return JsonResponse({
            "success": True,
            "updated_count": updated
        }, content_type='application/json')
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500, content_type='application/json')


@login_required(login_url="my-login")
def get_member_stats(request):
    """Üye için istatistikleri getir - DB'den gerçek veriler"""
    try:
        from django.db.models import Count, Q
        from django.utils import timezone
        from datetime import date
        
        # Aktif Günler: LoginActivity'den unique gün sayısı
        active_days = LoginActivity.objects.filter(user=request.user).values('login_date').distinct().count()
        
        # Sohbet Seansları: Kullanıcının mesaj gönderdiği unique gün sayısı
        chat_sessions = PsychologistMessage.objects.filter(
            user=request.user,
            sender='user'
        ).values('created_at__date').distinct().count()
        
        # Görev Sayısı: Psikologun verdiği toplam görev adedi
        task_count = Task.objects.filter(user=request.user).count()
        
        return JsonResponse({
            "success": True,
            "active_days": active_days,
            "chat_sessions": chat_sessions,
            "task_count": task_count
        }, content_type='application/json')
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500, content_type='application/json')


# ==========================================================
# === PSİKOLOG PANELİ YENİ API'LERİ ===
# ==========================================================

@psychologist_required
@require_GET
def get_private_notes(request):
    """Psikologun seçili kullanıcıya ait özel notunu getir"""
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': _('Kullanıcı ID gerekli.')}, status=400, content_type='application/json')
    try:
        target_user = User.objects.get(id=user_id)
        relation = PsychologistUserRelation.objects.filter(
            psychologist=request.user, user=target_user
        ).first()
        notes = relation.private_notes if relation else ''
        return JsonResponse({'success': True, 'notes': notes or ''}, content_type='application/json')
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': _('Kullanıcı bulunamadı.')}, status=404, content_type='application/json')
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500, content_type='application/json')


@psychologist_required
@require_POST
def save_private_notes(request):
    """Psikologun seçili kullanıcıya ait özel notunu kaydet"""
    import traceback as tb
    user_id = request.POST.get('user_id')
    notes = request.POST.get('notes', '').strip()
    if not user_id:
        return JsonResponse({'success': False, 'error': _('Kullanıcı ID gerekli.')}, status=400, content_type='application/json')
    try:
        target_user = User.objects.get(id=user_id)
        # Önce ilişkinin var olduğundan emin ol (yok ise oluştur)
        PsychologistUserRelation.objects.get_or_create(
            psychologist=request.user,
            user=target_user,
            defaults={'category': 'normal'}
        )
        # clear() ile aynı yaklaşımla güncelle — filter().update() doğrudan SQL UPDATE çalıştırır
        PsychologistUserRelation.objects.filter(
            psychologist=request.user,
            user=target_user
        ).update(private_notes=notes if notes else None)
        return JsonResponse({'success': True, 'message': _('Not kaydedildi.')}, content_type='application/json')
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': _('Kullanıcı bulunamadı.')}, status=404, content_type='application/json')
    except Exception as e:
        error_detail = tb.format_exc()
        return JsonResponse({'success': False, 'error': str(e), 'detail': error_detail[-500:]}, status=500, content_type='application/json')



@psychologist_required
@require_POST
def clear_private_notes(request):
    """Psikologun seçili kullanıcıya ait özel notunu temizle"""
    user_id = request.POST.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': _('Kullanıcı ID gerekli.')}, status=400, content_type='application/json')
    try:
        target_user = User.objects.get(id=user_id)
        PsychologistUserRelation.objects.filter(
            psychologist=request.user, user=target_user
        ).update(private_notes=None)
        return JsonResponse({'success': True, 'message': _('Not temizlendi.')}, content_type='application/json')
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': _('Kullanıcı bulunamadı.')}, status=404, content_type='application/json')
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500, content_type='application/json')


@psychologist_required
@require_POST
def update_user_category(request):
    """Kullanıcı kategorisini güncelle (acil / supheli / normal)"""
    import traceback as tb
    user_id = request.POST.get('user_id')
    category = request.POST.get('category', '').strip()
    valid_categories = {'acil', 'supheli', 'normal'}
    if not user_id or category not in valid_categories:
        return JsonResponse({'success': False, 'error': _('Geçersiz kullanıcı ID veya kategori.')}, status=400, content_type='application/json')
    try:
        target_user = User.objects.get(id=user_id)
        # Önce ilişkinin var olduğundan emin ol
        PsychologistUserRelation.objects.get_or_create(
            psychologist=request.user,
            user=target_user,
            defaults={'category': 'normal'}
        )
        # clear() ile aynı yaklaşım — filter().update() doğrudan SQL UPDATE
        PsychologistUserRelation.objects.filter(
            psychologist=request.user,
            user=target_user
        ).update(category=category)
        return JsonResponse({'success': True, 'category': category, 'message': _('Kategori güncellendi.')}, content_type='application/json')
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': _('Kullanıcı bulunamadı.')}, status=404, content_type='application/json')
    except Exception as e:
        error_detail = tb.format_exc()
        return JsonResponse({'success': False, 'error': str(e), 'detail': error_detail[-500:]}, status=500, content_type='application/json')


@psychologist_required
@require_GET
def get_user_usage_stats(request):
    """Seçili kullanıcının son 7 günlük giriş/kullanım verisi"""
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': _('Kullanıcı ID gerekli.')}, status=400, content_type='application/json')
    try:
        target_user = User.objects.get(id=user_id)
        from datetime import date, timedelta
        today = date.today()
        # Son 7 gün için tarih listesi oluştur (6 gün önce → bugün)
        days = [today - timedelta(days=i) for i in range(6, -1, -1)]
        # LoginActivity'den gerçek giriş kayıtlarını al
        login_set = set(
            LoginActivity.objects.filter(
                user=target_user,
                login_date__gte=days[0]
            ).values_list('login_date', flat=True)
        )
        chart_data = []
        for d in days:
            chart_data.append({
                'date': d.isoformat(),
                'label': d.strftime('%d/%m'),
                'day_name': ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'][d.weekday()],
                'logged_in': d in login_set,
                'sessions': 1 if d in login_set else 0,
            })
        total_active = sum(1 for d in chart_data if d['logged_in'])
        return JsonResponse({
            'success': True,
            'chart_data': chart_data,
            'total_active_days': total_active,
        }, content_type='application/json')
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': _('Kullanıcı bulunamadı.')}, status=404, content_type='application/json')
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500, content_type='application/json')


@psychologist_required
@require_POST
def bulk_notify(request):
    """
    Kategori bazlı toplu bildirim gönder.
    Psikologun seçtiği kategorilerdeki (acil/supheli/normal) kullanıcılara bildirim gönderir.
    """
    try:
        text = (request.POST.get('text') or '').strip()
        categories_raw = request.POST.getlist('categories[]')
        if not categories_raw:
            cat_str = request.POST.get('categories', '')
            categories_raw = [c.strip() for c in cat_str.split(',') if c.strip()]

        if not text:
            return JsonResponse({'success': False, 'error': _('Bildirim metni boş olamaz.')}, status=400, content_type='application/json')
        if not categories_raw:
            return JsonResponse({'success': False, 'error': _('En az bir kategori seçmelisiniz.')}, status=400, content_type='application/json')

        valid_categories = {'acil', 'supheli', 'normal'}
        categories = [c for c in categories_raw if c in valid_categories]
        if not categories:
            return JsonResponse({'success': False, 'error': _('Geçersiz kategori seçimi.')}, status=400, content_type='application/json')

        # Psikologun seçili kategorilerdeki kullanıcılarını bul
        target_relations = PsychologistUserRelation.objects.filter(
            psychologist=request.user,
            category__in=categories
        ).select_related('user')

        target_users = [rel.user for rel in target_relations]

        if not target_users:
            cat_labels = {'acil': 'Acil', 'supheli': 'Şüpheli', 'normal': 'Normal'}
            selected_labels = ', '.join([cat_labels.get(c, c) for c in categories])
            return JsonResponse({
                'success': False,
                'error': _('Seçilen kategorilerde ({}) kayıtlı kullanıcı bulunamadı.').format(selected_labels)
            }, status=404, content_type='application/json')

        # Toplu bildirim oluştur
        notifications = [
            Notification(user=u, text=text)
            for u in target_users
        ]
        Notification.objects.bulk_create(notifications)

        cat_labels = {'acil': 'Acil', 'supheli': 'Şüpheli', 'normal': 'Normal'}
        selected_labels = ', '.join([cat_labels.get(c, c) for c in categories])
        return JsonResponse({
            'success': True,
            'sent_count': len(target_users),
            'message': _('{} kategorisindeki {} kullanıcıya bildirim gönderildi.').format(
                selected_labels, len(target_users)
            )
        }, content_type='application/json')

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500, content_type='application/json')


# ==========================================================
# === GOREV TAMAMLAMA (UYE) ===
# ==========================================================

@require_POST
@login_required(login_url="my-login")
def complete_task(request):
    """Uye tarafindan gorev tamamlama"""
    task_id = request.POST.get('task_id')
    if not task_id:
        return JsonResponse({'success': False, 'error': _('Gorev ID gerekli.')}, status=400, content_type='application/json')
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        if not task.is_completed:
            task.is_completed = True
            task.completed_at = timezone.now()
            task.save(update_fields=['is_completed', 'completed_at'])
        return JsonResponse({'success': True, 'task_id': task.id, 'is_completed': True}, content_type='application/json')
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': _('Gorev bulunamadi.')}, status=404, content_type='application/json')
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500, content_type='application/json')


# ==========================================================
# === SEANS DEGERLENDIRME (PSIKOLOG) ===
# ==========================================================

@psychologist_required
@require_POST
def save_session_rating(request):
    """Psikolog icin gunluk seans degerlendirmesi kaydet/guncelle"""
    user_id = request.POST.get('user_id')
    rating_val = request.POST.get('rating')
    note_val = (request.POST.get('note') or '').strip()
    from datetime import date
    session_date_str = request.POST.get('session_date') or date.today().isoformat()

    if not user_id or not rating_val:
        return JsonResponse({'success': False, 'error': _('user_id ve rating gerekli.')}, status=400, content_type='application/json')
    try:
        rating_int = int(rating_val)
        if not (1 <= rating_int <= 10):
            return JsonResponse({'success': False, 'error': _('Rating 1-10 arasinda olmali.')}, status=400, content_type='application/json')
    except ValueError:
        return JsonResponse({'success': False, 'error': _('Gecersiz rating degeri.')}, status=400, content_type='application/json')

    try:
        from datetime import date as date_cls
        session_date = date_cls.fromisoformat(session_date_str)
    except ValueError:
        from datetime import date as date_cls
        session_date = date_cls.today()

    try:
        target_user = User.objects.get(id=user_id)
        rating_obj, created = SessionRating.objects.update_or_create(
            psychologist=request.user,
            user=target_user,
            session_date=session_date,
            defaults={'rating': rating_int, 'note': note_val or None}
        )
        return JsonResponse({
            'success': True,
            'created': created,
            'rating': rating_obj.rating,
            'session_date': rating_obj.session_date.isoformat(),
        }, content_type='application/json')
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': _('Kullanici bulunamadi.')}, status=404, content_type='application/json')
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500, content_type='application/json')


@psychologist_required
@require_GET
def get_session_ratings(request):
    """Psikolog icin belirli bir kullanicinin seans derecelendirme gecmisini getir (son 30 gun)"""
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': _('user_id gerekli.')}, status=400, content_type='application/json')
    try:
        target_user = User.objects.get(id=user_id)
        from datetime import date, timedelta
        since = date.today() - timedelta(days=30)
        ratings = SessionRating.objects.filter(
            psychologist=request.user,
            user=target_user,
            session_date__gte=since
        ).order_by('session_date')
        data = [{
            'date': r.session_date.isoformat(),
            'label': r.session_date.strftime('%d/%m'),
            'rating': r.rating,
            'note': r.note or ''
        } for r in ratings]
        return JsonResponse({'success': True, 'ratings': data}, content_type='application/json')
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': _('Kullanici bulunamadi.')}, status=404, content_type='application/json')
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500, content_type='application/json')


@psychologist_required
@require_GET
def get_user_assigned_tasks(request):
    """Psikolog icin belirli bir kullanicinin gorevlerini (tamamlanmis/bekleyen) getir"""
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'error': _('user_id gerekli.')}, status=400, content_type='application/json')
    try:
        target_user = User.objects.get(id=user_id)
        tasks = Task.objects.filter(user=target_user).order_by('-created_at')
        TASK_DISPLAY = {
            'breathing_exercise': 'Nefes Egzersizi',
            'meditation': 'Meditasyon',
            'daily_cards': 'Gunluk Kartlar',
            'support_wall': 'Destek Duvari',
        }
        data = [{
            'id': t.id,
            'text': t.text,
            'display_name': TASK_DISPLAY.get(t.text, t.text),
            'is_completed': t.is_completed,
            'created_at': timezone.localtime(t.created_at).strftime('%d.%m.%Y'),
            'completed_at': timezone.localtime(t.completed_at).strftime('%d.%m.%Y %H:%M') if t.completed_at else None,
        } for t in tasks]
        return JsonResponse({'success': True, 'tasks': data}, content_type='application/json')
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': _('Kullanici bulunamadi.')}, status=404, content_type='application/json')
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500, content_type='application/json')


# ==========================================================
# === FORUM (DESTEK DUVARI) API'LERI ===
# ==========================================================

@require_POST
@login_required(login_url="my-login")
def create_forum_post(request):
    """Yeni forum gonderisi olustur"""
    content = (request.POST.get('content') or '').strip()
    if not content:
        return JsonResponse({'success': False, 'error': _('Icerik bos olamaz.')}, status=400, content_type='application/json')
    post = ForumPost.objects.create(user=request.user, content=content)
    return JsonResponse({
        'success': True,
        'post': {
            'id': post.id,
            'content': post.content,
            'created_at': timezone.localtime(post.created_at).strftime('%d.%m.%Y %H:%M'),
            'likes_count': 0,
            'comment_count': 0,
        }
    }, content_type='application/json')


@require_POST
@login_required(login_url="my-login")
def like_forum_post(request):
    """Forum gonderi begen/begen-kaldir toggle"""
    post_id = request.POST.get('post_id')
    if not post_id:
        return JsonResponse({'success': False, 'error': _('post_id gerekli.')}, status=400, content_type='application/json')
    try:
        post = ForumPost.objects.get(id=post_id)
        like, created = ForumLike.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        post.likes_count = ForumLike.objects.filter(post=post).count()
        post.save(update_fields=['likes_count'])
        return JsonResponse({'success': True, 'liked': liked, 'likes_count': post.likes_count}, content_type='application/json')
    except ForumPost.DoesNotExist:
        return JsonResponse({'success': False, 'error': _('Gonderi bulunamadi.')}, status=404, content_type='application/json')
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500, content_type='application/json')


@require_POST
@login_required(login_url="my-login")
def add_forum_comment(request):
    """Forum gonderisine anonim yorum ekle"""
    post_id = request.POST.get('post_id')
    content = (request.POST.get('content') or '').strip()
    if not post_id or not content:
        return JsonResponse({'success': False, 'error': _('post_id ve icerik gerekli.')}, status=400, content_type='application/json')
    try:
        post = ForumPost.objects.get(id=post_id)
        comment = ForumComment.objects.create(post=post, user=request.user, content=content)
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'created_at': timezone.localtime(comment.created_at).strftime('%d.%m.%Y %H:%M'),
            }
        }, content_type='application/json')
    except ForumPost.DoesNotExist:
        return JsonResponse({'success': False, 'error': _('Gonderi bulunamadi.')}, status=404, content_type='application/json')
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500, content_type='application/json')


@require_GET
@login_required(login_url="my-login")
def get_forum_comments(request):
    """Belirli bir forum gonderisinin yorumlarini getir"""
    post_id = request.GET.get('post_id')
    if not post_id:
        return JsonResponse({'success': False, 'error': _('post_id gerekli.')}, status=400, content_type='application/json')
    try:
        post = ForumPost.objects.get(id=post_id)
        comments = post.comments.order_by('created_at')
        data = [{
            'id': c.id,
            'content': c.content,
            'created_at': timezone.localtime(c.created_at).strftime('%d.%m.%Y %H:%M'),
        } for c in comments]
        return JsonResponse({'success': True, 'comments': data}, content_type='application/json')
    except ForumPost.DoesNotExist:
        return JsonResponse({'success': False, 'error': _('Gonderi bulunamadi.')}, status=404, content_type='application/json')
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500, content_type='application/json')

@login_required
@require_POST
def delete_psychologist_message(request):
    """Belirli bir mesajı siler"""
    message_id = request.POST.get('message_id')
    try:
        from .models import PsychologistMessage
        msg = PsychologistMessage.objects.get(id=message_id)
        msg.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})