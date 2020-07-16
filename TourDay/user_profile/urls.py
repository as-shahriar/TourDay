from django.urls import path
from user_profile import views


urlpatterns = [
    path("profile/", views.edit_profile, name="edit_profile"),
    path("profile/<param>", views.add_info, name="edit_profile_ajax"),


]
