from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData
from .models import Order, OrderItem, Product
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def store(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {
        'products':products, 
        'cartItems':cartItems,
    }
    return render(request, 'ecommerce/store.html', context)

def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items':items, 
        'order':order,
        'cartItems':cartItems,
    }
    return render(request, 'ecommerce/cart.html', context)

@login_required
def checkout(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    print(order)

    if request.method == 'POST' and 'checkout' in request.POST:
        
        ord = Order.objects.create(customer=request.user, total_money=order['get_cart_total'], 
        total_items=order['get_cart_items'], order_id=101)
        ord.save()

        for item in items:
            product = Product.objects.get(id=item['product']['id'])
            orders = Order.objects.filter(customer=request.user) 
            for order in orders:
                if order.status == 'Pending':
                    order_item = OrderItem.objects.create(order=order,product=product,quantity=item['quantity'])
                    order_item.save()
   
    context = {
    'items':items,
    'order':order,
    'cartItems':cartItems
    }
    return render(request, 'ecommerce/checkout.html', context)
