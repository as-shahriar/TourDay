from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData
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


def checkout(request):

	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {
        'items':items,
        'order':order,
        'cartItems':cartItems
    }
	return render(request, 'ecommerce/checkout.html', context)
