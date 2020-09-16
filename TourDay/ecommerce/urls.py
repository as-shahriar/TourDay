from django.urls import path
from ecommerce.views import store,cart

urlpatterns = [
    path('', store, name='store' ),
    path('cart/', cart, name="cart"),
]