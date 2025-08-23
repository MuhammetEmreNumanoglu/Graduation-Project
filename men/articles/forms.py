from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from . models import Article,Profile
from .models import EmergencyContact
from django.utils.translation import gettext_lazy as _




class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title','content',]
        exclude = ['user']

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_('E-posta'))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': _('Kullanıcı Adı'),
            'email': _('E-posta'),
            'password1': _('Şifre'),
            'password2': _('Şifre Tekrar'),
        }
        help_texts = {
            'username': _('150 karakter ya da daha az olmalı. Sadece harfler, rakamlar ve @/./+/-/_ karakterleri kullanılabilir.'),
            'password1': _('Şifreniz en az 8 karakter içermelidir.'),
            'password2': _('Doğrulama için aynı şifreyi tekrar girin.'),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Username benzersiz olsun
            if User.objects.filter(username__iexact=username).exists():
                raise ValidationError(_('Bu kullanıcı adı zaten alınmış.'))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Email benzersiz olsun
            if User.objects.filter(email__iexact=email).exists():
                raise ValidationError(_('Bu e-posta zaten alınmış.'))
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(), label=_('Kullanıcı Adı'))
    password = forms.CharField(widget=PasswordInput, label=_('Şifre'))


class UpdateUserForm(forms.ModelForm):
    password = None 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = _("Kullanıcı Adı")
        self.fields['email'].label = _("Email")
    class Meta:
        model = User 
        fields = ["username", "email",]
        exclude = [ "password1", "password2"]
        labels = {
            'username': _('Kullanıcı Adı'),
            'email': _('E-posta'),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            qs = User.objects.filter(username__iexact=username)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError(_('Bu kullanıcı adı zaten alınmış.'))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email__iexact=email)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError(_('Bu e-posta zaten alınmış.'))
        return email

class UpdateProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-file'}),label=_('Profil Fotoğrafı'))
    class Meta:
        model = Profile
        fields = ['profile_pic',]
        labels = {
            'profile_pic': _('Profil Fotoğrafı'),
        }

class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        labels = {
            'title': _('Başlık'),
            'content': _('İçerik'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Başlık giriniz...')}),
            'content': forms.Textarea(attrs={'placeholder': _('İçerik giriniz...')}),
        }

class UpdateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        labels = {
            'title': _('Başlık'),
            'content': _('İçerik'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Başlık giriniz...')}),
            'content': forms.Textarea(attrs={'placeholder': _('İçerik giriniz...')}),
        }


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['relation', 'full_name', 'phone']
        labels = {
            'relation': _('Yakınlık'),
            'full_name': _('Ad Soyad'),
            'phone': _('Telefon Numarası'),
        }
        widgets = {
            'relation': forms.TextInput(attrs={'placeholder': _('Örn: Anne, Baba, Arkadaş')}),
            'full_name': forms.TextInput(attrs={'placeholder': _('Ad Soyad')}),
            'phone': forms.TextInput(attrs={'placeholder': _('05xx xxx xx xx')}),
        }
    def clean_phone(self):
        raw = (self.cleaned_data.get('phone') or '').strip()
        if not raw:
            raise ValidationError(_('Telefon numarası gerekli.'))
        digits = ''.join(ch for ch in raw if ch.isdigit())
        if len(digits) != 11:
            raise ValidationError(_('Telefon numarası 11 haneli olmalıdır.'))
        return digits

     