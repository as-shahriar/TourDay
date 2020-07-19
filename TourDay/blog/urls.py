
from django.urls import path
from blog.views import search, home, details, addPost




urlpatterns = [
  path("",search,name="search_page"),
  path('blog/home', home, name='blog_home' ),
  path('blog/details', details, name='details' ),
  path('blog/addpost', addPost, name='addpost' ),
]
