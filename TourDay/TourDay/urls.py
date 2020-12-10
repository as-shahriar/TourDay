
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('_auth.urls')),
    path('', include('blog.urls')),
    path('', include('user_profile.urls')),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    path('event/', include('event.urls')),
    path('shop/', include('ecommerce.urls')),
    path('api/', include('api.urls')),
    path('api/shop/', include('ecommerce.api.urls')),
    path('api/blog/', include('blog.api.urls')),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = '_auth.views.error_404_view'
