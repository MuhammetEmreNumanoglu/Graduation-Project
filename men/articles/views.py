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
from .models import Article, Profile, ChatHistory, ChatHistoryContent, Like, EmergencyContact, UserAIAssistantProfile, Task, Notification, PsychologistMessage
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
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('psychologist-login')
        
        # Profile'dan role kontrolü
        try:
            profile = Profile.objects.get(user=request.user)
            if profile.role != 'psychologist':
                messages.error(request, _("Bu sayfaya erişim için psikolog hesabı gereklidir."))
                return redirect('psychologist-login')
        except Profile.DoesNotExist:
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
    if request.method == "POST":
        content = request.POST.get("storyText")
        if content and len(content.strip()) > 0:
            ChatHistoryContent.objects.create(
                role="user",
                content=content.strip(),
                chat_history=ChatHistory.objects.get_or_create(user=request.user)[0]
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": True, "message": _("Mesaj eklendi.")})
            return redirect("destek-duvari")

    user_chat_history = ChatHistory.objects.get_or_create(user=request.user)[0]
    all_messages = ChatHistoryContent.objects.filter(chat_history=user_chat_history, role='user').order_by('-created_at')
    paginator = Paginator(all_messages, 3)
    page = int(request.GET.get('page', 1))
    messages = paginator.get_page(page)
    liked_messages = set(Like.objects.filter(user=request.user, story__in=messages.object_list).values_list('story_id', flat=True))
    profile_pic = Profile.objects.filter(user=request.user).first()
    if not profile_pic:
        profile_pic = Profile.objects.create(user=request.user)
    return render(request, "articles/destek-duvari.html", {
        "messages": messages,
        "liked_messages": liked_messages,
        "page": page,
        "total_pages": paginator.num_pages
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
    field = request.GET.get('field')
    value = request.GET.get('value', '').strip()
    current_user_id = None
    if request.user.is_authenticated:
        current_user_id = request.user.id
    if not field or not value:
        return JsonResponse({'available': False, 'error': _('Geçersiz istek')}, status=400)
    if field == 'username':
        qs = User.objects.filter(username__iexact=value)
        if current_user_id:
            qs = qs.exclude(pk=current_user_id)
        return JsonResponse({'available': not qs.exists()})
    elif field == 'email':
        qs = User.objects.filter(email__iexact=value)
        if current_user_id:
            qs = qs.exclude(pk=current_user_id)
        return JsonResponse({'available': not qs.exists()})
    else:
        return JsonResponse({'available': False, 'error': _('Bilinmeyen alan')}, status=400)

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
    
    # Her kullanıcı için son mesaj zamanını hesapla
    users_with_last_message = []
    for user in member_users:
        last_message = PsychologistMessage.objects.filter(user=user).order_by('-created_at').first()
        users_with_last_message.append({
            'user': user,
            'last_message_time': last_message.created_at if last_message else None
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
    
    context = {
        'target_user': target_user,
        'messages': messages
    }
    return render(request, "articles/psychologist-chat.html", context)


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
        return JsonResponse({"success": True, "task_id": task.id, "message": _("Görev başarıyla gönderildi.")})
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
            "created_at": message.created_at.strftime("%d.%m.%Y %H:%M"),
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
        "created_at": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
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
            'created_at': msg.created_at.strftime("%Y-%m-%d %H:%M:%S"),
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
            'created_at': msg.created_at.strftime("%d.%m.%Y %H:%M"),
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
        'created_at': task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
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
        'created_at': notif.created_at.strftime("%Y-%m-%d %H:%M:%S"),
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