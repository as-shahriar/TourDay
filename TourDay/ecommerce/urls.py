from django.urls import path
from ecommerce.views import (
    store,cart,checkout, staff_pages, product_table, order_table, order_details, user_order, product_edit)

urlpatterns = [
    path('', store, name='store' ),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('staff/', staff_pages, name='staff_pages'),
    path('allproduct/', product_table, name='all_product'),
    path('product/edit/', product_edit, name='product_edit'),
    path('allorder/', order_table, name='all_order'),
    path('order/details/<int:id>', order_details, name='order_details'),
    path('user/order/', user_order, name='user_order')

]