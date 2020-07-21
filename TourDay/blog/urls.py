
from django.urls import path
from blog.views import search, home, details, addPost
from ckeditor_uploader import views as uploader_views
from django.views.decorators.cache import never_cache


urlpatterns = [

  path('ckeditor/upload/', uploader_views.upload, name='ckeditor_upload'),
  path('ckeditor/browse/', never_cache(uploader_views.browse), name='ckeditor_browse'),


  path("",search,name="search_page"),
  path('blog/home', home, name='blog_home' ),
  path('blog/details/<int:id>', details, name='blog_details' ),
  path('blog/addpost', addPost, name='addpost' ),
 
]
