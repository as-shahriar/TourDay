
from django.urls import path
from blog.views import search, home, details




urlpatterns = [
  path("",search,name="search_page"),
  path('blog/home', home, name='home' ),
  path('blog/details', details, name='details' ),
   
]
