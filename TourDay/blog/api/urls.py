from django.urls import path
from .views import (api_home, api_details, api_user_post, api_division_post, api_addpost, api_blogEdit, api_blogDelete)

urlpatterns = [
    path('home/', api_home, name='home'),
    path('details/<int:id>', api_details, name='api_details'),
    path('user/<slug>', api_user_post, name='api_user_post'),
    path('division/<slug>', api_division_post, name='api_division_post'),
    path('addpost/', api_addpost, name='api_addpost'),
    path('edit/<int:id>', api_blogEdit, name='api_blogEdit'),
    path('delete/<int:id>', api_blogDelete, name='api_blogDelete'),
]