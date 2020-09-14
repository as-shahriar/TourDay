from django.urls import path
from ecommerce.views import index

urlpatterns = [
    path('', index, name='index' ),
]