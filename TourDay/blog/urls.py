
from django.urls import path
from blog.views import search, home, addPost, details, user_post, blog_edit, blog_delete, division_post

from ckeditor_uploader import views as uploader_views
from django.views.decorators.cache import never_cache


urlpatterns = [

  path('ckeditor/upload/', uploader_views.upload, name='ckeditor_upload'), 
  path('ckeditor/browse/', never_cache(uploader_views.browse), name='ckeditor_browse'),


  path("",search,name="search_page"),
  path('blog/home', home, name='blog_home' ),
  path('blog/details/<int:id>', details, name='blog_details' ),
  path('blog/addpost', addPost, name='addpost' ),
  path('blog/edit/<int:id>', blog_edit, name='blog_edit' ),
  path('blog/delete/<int:id>', blog_delete, name='blog_delete' ),
  path('blog/user/<slug>', user_post, name='user_post' ),
  path('blog/division/<slug>', division_post, name='division_post'),
  
]
