
from django.urls import path
from _auth.views import loginView

urlpatterns = [
   path('login/',loginView,name='login_page'),
]
