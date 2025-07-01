from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from . models import Article,Profile
from django.utils.translation import gettext_lazy as _




class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title','content',]
        exclude = ['user']

class CreateUserForm(UserCreationForm):
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


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(), label=_('Kullanıcı Adı'))
    password = forms.CharField(widget=PasswordInput, label=_('Şifre'))


class UpdateUserForm(forms.ModelForm):
    password = None 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Kullanıcı Adı"
        self.fields['email'].label="Email"
    class Meta:
        model = User 
        fields = ["username", "email",]
        exclude = [ "password1", "password2"]
        labels = {
            'username': _('Kullanıcı Adı'),
            'email': _('E-posta'),
        }

class UpdateProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control-file'}),label='Profil Fotoğrafı')
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

     