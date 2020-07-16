from django.contrib import admin
from .models import Profile
# Register your models here.


class ProfileConf(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'id')


admin.site.register(Profile, ProfileConf)
