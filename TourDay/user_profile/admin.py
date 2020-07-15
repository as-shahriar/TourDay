from django.contrib import admin
from .models import Profile
# Register your models here.


class ProfileConf(admin.ModelAdmin):
    list_display = ('name', 'user', 'email')


admin.site.register(Profile, ProfileConf)
