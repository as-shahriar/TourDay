from django.urls import path
from user_profile import views


urlpatterns = [
    path("profile/", views.edit_profile, name="edit_profile"),
    path("profile/<param>", views.add_info, name="edit_profile_ajax"),
    path("u/<username>", views.portfolio, name="portfolio"),
    path("get_post/<str:username>", views.PostList.as_view()),
    path("like/", views.like_event),
    path("add_post/", views.add_post),
    path("delete_post/", views.delete_post),
    path("visited/<int:id>", views.get_map_data)

]
