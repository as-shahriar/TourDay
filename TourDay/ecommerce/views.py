from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData
from .models import Order, OrderItem, Product
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from random import randint
from django.db.models import Q
# Create your views here.



def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


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
    profile = get_object_or_404(Profile, user=request.user)
    
    if profile == None:
        return redirect(f'/u/request.user')

    criterion1 = Q(customer__exact=request.user)
    criterion2 = Q(status__exact="Pending")
    pending_check = bool(Order.objects.filter(criterion1 & criterion2))
    print(pending_check)
    
    if pending_check:
       url = '/ecommerce/'
       resp_body = '<script>alert("Your already have a pending items!");\
                    window.location="%s"</script>' % url
       return HttpResponse(resp_body)
       
    else:
        if request.method == 'POST' and 'checkout' in request.POST:
            
            random_order_id = int(random_with_N_digits(8))

            ord = Order.objects.create(customer=request.user, total_money=order['get_cart_total'], 
            total_items=order['get_cart_items'], order_id=random_order_id)
            ord.save()

            for item in items:
                product = Product.objects.get(id=item['product']['id'])
                orders = Order.objects.filter(customer=request.user) 
                for order in orders:
                    if order.status == 'Pending':
                        order_item = OrderItem.objects.create(order=order,product=product,quantity=item['quantity'])
                        order_item.save()
            
            shipping = ShippingAddress()
            
            order = Order.objects.get(order_id=random_order_id)

            shipping.order = order
            shipping.customer = request.user
            shipping.PhoneNo = request.POST.get('phone').strip()
            shipping.allPhoneNo = request.POST.get('al_phone').strip()
            shipping.address = request.POST.get('address').strip()
            shipping.city = request.POST.get('city').strip()
            shipping.state = request.POST.get('state').strip()
            shipping.zipcode = request.POST.get('zipcode').strip()
            shipping.save()

            pay = payment()

            pay.customer = request.user
            pay.order = order
            pay.method = request.POST.get('colorCheckbox')
            if request.POST.get('payment_mtd') == 'checked':
                pay.payment_method = None
            else:
                pay.payment_method = request.POST.get('payment_mtd')
            pay.PhoneNo = request.POST.get('pay_phone_no')
            pay.trxId = request.POST.get('trxid')
            pay.save()
        
      
   
    context = {
    'items':items,
    'order':order,
    'cartItems':cartItems,
    'profile' : profile,
    
    }
    return render(request, 'ecommerce/checkout.html', context)

def edit(request):
    return render(request, 'ecommerce/stuff_page/main.html')

def table(request):

    product = Product.objects.all().order_by('-id')

    context = {
        'product' : product,
    }

    return render(request, 'ecommerce/stuff_page/product_table.html', context)


def order_table(request):

    order = Order.objects.all().order_by('-id')

    context = {
        'order' : order,
    }

    return render(request, 'ecommerce/stuff_page/order_table.html', context)

def order_details(request, id):

    order = Order.objects.get(id=id)
    order_item = OrderItem.objects.filter(order=order).order_by('quantity')
    shipping = ShippingAddress.objects.get(order=order)
    paymt = payment.objects.get(order=order)
    print(order_item)

    if request.method == 'POST' and 'order_submit' in request.POST:
        order.status = request.POST.get('payment_mtd')
        order.save()
        return redirect('all_order')

    context = {
        'order' : order,
        'order_item' : order_item,
        'shipping' : shipping,
        'paymt' : paymt,
    }
    
    return render(request, 'ecommerce/stuff_page/order_details.html', context)