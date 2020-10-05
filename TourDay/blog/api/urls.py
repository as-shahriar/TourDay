from django.urls import path
from .views import (api_home, api_details, api_user_post, api_division_post, api_addpost, api_blogEdit, 
    api_blogDelete, api_doc, api_BlogSearch,

)

urlpatterns = [

    path('', api_doc, name='Blog_api_doc'),

    path('query', api_BlogSearch.as_view(), name='api_BlogSearch'),
    path('allpost/', api_home, name='home'),
    path('details/<int:id>', api_details, name='api_details'),
    path('user/<slug>', api_user_post, name='api_user_post'),
    path('division/<slug>', api_division_post, name='api_division_post'),
    path('addpost/', api_addpost, name='api_addpost'),
    path('edit/<int:id>', api_blogEdit, name='api_blogEdit'),
    path('delete/<int:id>', api_blogDelete, name='api_blogDelete'),
]