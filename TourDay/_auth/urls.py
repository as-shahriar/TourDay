
from django.urls import path
from _auth.views import (
    loginView,signupView,
    forgetPasswordView,resetPasswordView,
    ajax_signup,ajax_forgetpassword,ajax_resetpassword,
    checkusername,checkemail,
    id_logout)




urlpatterns = [
   path('login/',loginView,name='login_page'),
    path('signup/',signupView,name='signup_page'),
    path('forget-password/',forgetPasswordView,name="forget_password_page"),
    path('reset-password/<slug>',resetPasswordView,name="reset_password_page"), 
    path('logout/',id_logout,name="logout"),
    path('checkusername',checkusername),
    path('checkemail',checkemail),
#Ajax Urls

    path('ajaxsignup',ajax_signup),
    path('ajaxforget',ajax_forgetpassword),
    path("ajaxreset",ajax_resetpassword),
]
