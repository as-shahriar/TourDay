from django.urls import path
from ecommerce.views import store,cart,checkout, staff_pages, table, order_table, order_details, user_order

urlpatterns = [
    path('', store, name='store' ),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('staff/', staff_pages, name='staff_pages'),
    path('allproduct/', table, name='all_product'),
    path('allorder/', order_table, name='all_order'),
    path('order/details/<int:id>', order_details, name='order_details'),
    path('user/order/', user_order, name='user_order')

]