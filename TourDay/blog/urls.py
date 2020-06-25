
from django.urls import path
from blog.views import search




urlpatterns = [
  path("",search,name="search_page")
   
]
