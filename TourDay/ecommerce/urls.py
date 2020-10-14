from django.urls import path
from ecommerce.views import store,cart,checkout, edit, table, order_table, order_details

urlpatterns = [
    path('', store, name='store' ),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('edit/', edit, name='edit'),
    path('product/', table, name='table'),
    path('allorder/', order_table, name='all_order'),
    path('order/details/<int:id>', order_details, name='order_details'),
]