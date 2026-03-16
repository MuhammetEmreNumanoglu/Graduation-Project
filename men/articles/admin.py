from django.contrib import admin
from .models import Article, Profile, DailyMood
# Register your models here.

admin.site.register(Article)
admin.site.register(Profile)
admin.site.register(DailyMood)