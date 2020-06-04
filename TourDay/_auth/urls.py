
from django.urls import path
from _auth.views import loginView,signupView

urlpatterns = [
   path('login/',loginView,name='login_page'),
    path('signup/',signupView,name='signup_page'),
]
