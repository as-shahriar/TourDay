
from django.urls import path
from _auth.views import loginView,signupView,forgetPasswordView,resetPasswordView

urlpatterns = [
   path('login/',loginView,name='login_page'),
    path('signup/',signupView,name='signup_page'),
    path('forget-password/',forgetPasswordView,name="forget_password_page"),
    path('reset-password/',resetPasswordView,name="reset_password_page"),
]
