from django.urls import path
from ecommerce.views import store,cart,checkout, edit, table, order_table

urlpatterns = [
    path('', store, name='store' ),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('edit/', edit, name='edit'),
    path('product/', table, name='table'),
    path('order/', order_table, name='order'),

]