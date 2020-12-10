from django.urls import path
from .views import product_details, product_home, order_details, all_category, category_product,search_product

urlpatterns = [
    path('product/details/<int:id>', product_details, name='product_details'),
    path('allproduct/',product_home, name='product_home'),
    path('order/user/', order_details, name='order_details'),
    path('allcategory/', all_category, name='allcategory'),
    path('category', category_product.as_view(), name='category_product'),
    path('search/product', search_product.as_view(), name='search_product'),
]