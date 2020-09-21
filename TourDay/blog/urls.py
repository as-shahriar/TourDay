
from django.urls import path
from blog.views import (search, 
    home, addPost, details, user_post, blog_edit, blog_delete, division_post, blog_search, api_home, api_details,
    api_user_post, api_division_post,
    )

from ckeditor_uploader import views as uploader_views
from django.views.decorators.cache import never_cache


urlpatterns = [

    path('ckeditor/upload/', uploader_views.upload, name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(uploader_views.browse),
         name='ckeditor_browse'),


    path('blog/search/', blog_search, name='blog_search'),
    path("", search, name="search_page"),
    path('blog', home, name='blog_home'),
    path('blog/details/<int:id>', details, name='blog_details'),
    path('blog/addpost', addPost, name='addpost'),
    path('blog/edit/<int:id>', blog_edit, name='blog_edit'),
    path('blog/delete/<int:id>', blog_delete, name='blog_delete'),
    path('blog/user/<slug>', user_post, name='user_post'),
    path('blog/division/<slug>', division_post, name='division_post'),


    # api
    path('blog/api', api_home, name='api_home'),
    path('blog/api/details/<int:id>', api_details, name='api_details'),
    path('blog/api/user/<slug>', api_user_post, name='api_user_post'),
    path('blog/api/division/<slug>', api_division_post, name='api_division_post'),
    # path('blog/api/addpost', api_addpost, name='api_addpost'),
]
