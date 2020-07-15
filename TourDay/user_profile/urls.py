from django.urls import path
from user_profile import views


urlpatterns = [
    path("profile/", views.edit_profile, name="edit_profile")

]
