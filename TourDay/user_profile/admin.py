from django.contrib import admin
from .models import Profile, Post
# Register your models here.


class ProfileConf(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'id')


class PostConf(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')


admin.site.register(Profile, ProfileConf)

admin.site.register(Post, PostConf)
