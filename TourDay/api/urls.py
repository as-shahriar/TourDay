from django.urls import path, include
from api import auth, profile, views
from _auth.views import forgetPasswordView, resetPasswordView
from user_profile.views import PostList
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="api/doc.html"), name="api_doc"),
    path('auth/', include('rest_auth.urls')),
    path('auth/signup/', auth.Signup.as_view()),
    path('profile/', profile.ProfileView.as_view()),
    path('get_posts/<str:username>', PostList.as_view()),
    path('post/', profile.PostWrite.as_view()),
    path('post_delete/', profile.PostDelete.as_view()),
    path('user/<str:username>', profile.UserDetails.as_view()),
    path('post/like/', profile.LikePost.as_view()),
    path('forget_password/', forgetPasswordView),
    path('reset_password/<str:slug>/', resetPasswordView),


    path('map/<str:username>', views.map),

]
