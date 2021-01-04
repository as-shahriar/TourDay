from django.contrib import admin
from blog.models import blogPost



class BlogPostConf(admin.ModelAdmin):
    list_display = ('title', 'blog_user',"division")


admin.site.register(blogPost, BlogPostConf)