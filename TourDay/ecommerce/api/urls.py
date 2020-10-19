from django.urls import path
from .views import product_details

urlpatterns = [
    path('product/details/<int:id>', product_details, name='product_details'),
]