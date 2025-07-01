from django.shortcuts import render, HttpResponse, redirect
from .forms import CreateUserForm, LoginForm, ArticleForm, UpdateUserForm,UpdateProfileForm
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import StreamingHttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .ai_wrapper import LLMClient
from .models import Article, Profile, ChatHistory, ChatHistoryContent, Like
from django.http import JsonResponse
from django.utils import translation
from django.conf import settings
from django.urls import reverse
from django.utils.translation import get_language, gettext as _
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import ChatHistory, ChatHistoryContent
import json
import uuid
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator


# Create your views here.


def homepage(request):
    return render(request, "articles/index.html")


def register(request):
    form = CreateUserForm(request.POST)
    if form.is_valid():
        current_user = form.save(commit=False)
        form.save()
        profile = Profile.objects.create(user=current_user)
        messages.success(request, "Kullanıcı Oluşturuldu!")
        return redirect("my-login")
    context = {"RegistrationForm": form}
    return render(request, "articles/register.html", context)


def my_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                active_language = get_language()
                dashboard_url = reverse("dashboard")
                if active_language != settings.LANGUAGE_CODE:
                    pass
                
                return redirect(dashboard_url)
    context = {"LoginForm": form}
    return render(request, "articles/my-login.html", context)


@login_required(login_url="my-login")
def dashboard(request):
    profile_pic = Profile.objects.filter(user=request.user).first()
    if not profile_pic:
        profile_pic = Profile.objects.create(user=request.user)
    context = {'profilePic': profile_pic}
    return render(request, "articles/dashboard.html", context)

@login_required(login_url="my-login")
def stream_llm_response(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Only POST allowed.")

    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message")
        history_id = data.get("history_id")

        if not history_id:
            history_id = str(uuid.uuid4())
            chat_history = ChatHistory.objects.create(
                user=request.user,
                history_id=history_id,
                title=message[:40]
            )
        else:
            chat_history = ChatHistory.objects.filter(history_id=history_id, user=request.user).first()
            if not chat_history:
                return JsonResponse({"error": "Geçersiz history_id"}, status=400)

        ChatHistoryContent.objects.create(
            chat_history=chat_history,
            role="user",
            content=message
        )

        llm = LLMClient(base_url="http://localhost:8008/api/llm", api_key="231")

        stream = False

        exists_history = ChatHistoryContent.objects.filter(chat_history=chat_history)
        history = [{"role": msg.role, "content": msg.content} for msg in exists_history]

        response_generator = llm.generate(
            history=history,
            model="llama-3.3-70b-versatile",
            provider="groq",
            stream=stream
        )

        def event_stream():
            for chunk in response_generator:
                yield f"data: {chunk}\n\n"

        if stream:
            return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        else:
            response_content = response_generator.get('content')

            ChatHistoryContent.objects.create(
                chat_history=chat_history,
                role="assistant",
                content=response_content
            )
            return JsonResponse({"content": response_content, "history_id": history_id})


def user_logout(request):
    auth.logout(request)
    return redirect("")


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
    form = UpdateUserForm(instance=request.user)
    profile = Profile.objects.filter(user=request.user).first()
    form_2 = UpdateProfileForm(instance=profile)
    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=request.user)
        form_2 = UpdateProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect("dashboard")
        if form_2.is_valid():
            form_2.save()
            return redirect("dashboard")

    context = {"UserUpdateForm": form, 'ProfileUpdateForm': form_2}
    return render(request, "articles/profile-management.html", context)


@login_required(login_url="my-login")
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Hesabınız başarıyla silindi.")
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
    chat_history, created = ChatHistory.objects.get_or_create(user=request.user, defaults={"history_id": str(request.user.id)})

    if request.method == "POST":
        content = request.POST.get("storyText")
        if content and len(content.strip()) > 0:
            ChatHistoryContent.objects.create(
                role="user",
                content=content.strip(),
                chat_history=chat_history
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": True, "message": "Mesaj eklendi."})
            return redirect("destek-duvari")

    all_messages = ChatHistoryContent.objects.filter(chat_history=chat_history).order_by('-likes', '-id')
    paginator = Paginator(all_messages, 3)
    page = int(request.GET.get('page', 1))
    messages = paginator.get_page(page)
    liked_messages = set(Like.objects.filter(user=request.user, story__in=messages).values_list('story_id', flat=True))
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
                messages.error(request, _('Please fill in all fields'))
                return redirect('profile-management')
            
            user = request.user
            if user.check_password(current_password):
                if current_password == new_password:
                    messages.error(request, _('New password cannot be the same as current password'))
                    return redirect('profile-management')
                
                try:
                    validate_password(new_password, user)
                    user.set_password(new_password)
                    user.save()
                    auth.logout(request)
                    messages.success(request, _('Your password has been successfully updated. Please login with your new password.'))
                    return redirect('my-login')
                except ValidationError as e:
                    messages.error(request, str(e))
                    return redirect('profile-management')
            else:
                messages.error(request, _('Current password is incorrect'))
                return redirect('profile-management')
                
        except Exception as e:
            messages.error(request, str(e))
            return redirect('profile-management')
    
    return redirect('profile-management')

def contact(request):
    return render(request, "articles/contact.html")

def anasayfa(request):
    return render(request, "articles/anasayfa.html")

def meditasyon(request):
    return render(request, 'articles/meditasyon.html')

def nefes_egzersizi(request):
    return render(request, 'articles/nefes-egzersizi.html')

def meditasyon_audio(request, audio_id):
    audio_map = {
        'rain': {
            'title': 'Derin Uyku İçin Yağmur',
            'image_url': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80',
            'audio_url': 'https://cdn.pixabay.com/audio/2022/07/26/audio_124bfa8c7b.mp3',  # Yağmur sesi (Pixabay)
        },
        'waves': {
            'title': 'Stres Azaltan Dalgalar',
            'image_url': 'https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80',
            'audio_url': 'https://cdn.pixabay.com/audio/2022/07/26/audio_124bfa8c7b.mp3',  # Dalgalar için örnek (değiştirilebilir)
        },
        'morning': {
            'title': 'Sabah Esnemesi',
            'image_url': 'https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=400&q=80',
            'audio_url': 'https://cdn.pixabay.com/audio/2022/03/15/audio_115b9b4e3b.mp3',  # Hafif müzik (Pixabay)
        },
        'piano': {
            'title': 'Odaklanma Piyanosu',
            'image_url': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80',
            'audio_url': 'https://cdn.pixabay.com/audio/2022/10/16/audio_12b6b1b7b2.mp3',  # Piyano (Pixabay)
        },
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
                return JsonResponse({
                    'success': True,
                    'message': 'Profil fotoğrafı başarıyla güncellendi!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Fotoğraf dosyası bulunamadı.'
                }, status=400)
                
        except Profile.DoesNotExist:
            # Eğer profil yoksa oluştur
            profile = Profile.objects.create(user=request.user)
            if 'profile_photo' in request.FILES:
                profile.avatar = request.FILES['profile_photo']
                profile.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Profil fotoğrafı başarıyla güncellendi!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Fotoğraf dosyası bulunamadı.'
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Bir hata oluştu: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Sadece POST istekleri kabul edilir.'
    }, status=405)

def responsive(request):
    return render(request, 'articles/responsive.html')

@require_POST
@login_required(login_url="my-login")
def like_story(request):
    story_id = request.POST.get("story_id")
    try:
        story = ChatHistoryContent.objects.get(id=story_id)
        like, created = Like.objects.get_or_create(user=request.user, story=story)
        if not created:
            # Zaten like'ladıysa, unlike yap
            like.delete()
            story.likes = Like.objects.filter(story=story).count()
            story.save()
            return JsonResponse({"success": True, "likes": story.likes, "liked": False})
        else:
            # Like ekle
            story.likes = Like.objects.filter(story=story).count()
            story.save()
            return JsonResponse({"success": True, "likes": story.likes, "liked": True})
    except ChatHistoryContent.DoesNotExist:
        return JsonResponse({"success": False, "error": "Mesaj bulunamadı."}, status=404)

