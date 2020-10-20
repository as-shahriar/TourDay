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
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required

import os
from PIL import Image
from TourDay.settings import MEDIA_DIR


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

    product_type = Product_type.objects.all().order_by('-id')
    
    products = Product.objects.all().order_by('-id')
    paginator = Paginator(products, 12)  # Show 12 obj per page

    page = request.GET.get('page')
    products = paginator.get_page(page)


    context = {

        'product_type' :  product_type,
        'products':products, 
        'cartItems':cartItems,
    }
    return render(request, 'ecommerce/store.html', context)

def cart(request):
    
    data = cartData(request)

    product_type = Product_type.objects.all().order_by('-id')

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items':items, 
        'order':order,
        'cartItems':cartItems,
        'product_type' : product_type,
    }
    return render(request, 'ecommerce/cart.html', context)

@login_required
def checkout(request):

    data = cartData(request)

    product_type = Product_type.objects.all().order_by('-id')

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    profile = get_object_or_404(Profile, user=request.user)

    if order['get_cart_total'] == 0 or order['get_cart_items'] == 0:
        return redirect('cart')
    
    if profile == None:
        return redirect(f'/u/request.user')

    criterion1 = Q(customer__exact=request.user)
    criterion2 = Q(status__exact="Pending")
    pending_check = bool(Order.objects.filter(criterion1 & criterion2))
    
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
    'product_type' : product_type,
    
    }
    return render(request, 'ecommerce/checkout.html', context)

@staff_member_required
def staff_pages(request):

    return render(request, 'ecommerce/stuff_page/main.html')

@staff_member_required
def product_table(request):

    product = Product.objects.all().order_by('-id')
    
    paginator = Paginator(product, 5)  # Show 5 obj per page

    page = request.GET.get('page')
    product = paginator.get_page(page)

    context = {
        'product' : product,
    }

    return render(request, 'ecommerce/stuff_page/product_table.html', context)

@staff_member_required
def add_product(request):

    product_type = Product_type.objects.all().order_by('-id')
    product = Product()

    if request.method == 'POST' and 'add_product' in request.POST:
        product.name = request.POST.get('product_name').strip()
        product.price =  request.POST.get('product_price').strip()
        product.product_type = request.POST.get('product_type').strip()
        product.discription = request.POST.get('product_dis').strip()
        product.image = request.FILES.get('product_img')

        product.save()
        return redirect('all_product')

    context = {

        'product_type' : product_type,
    }

    return render(request, 'ecommerce/stuff_page/add_product.html', context)

@staff_member_required
def product_delete(request, id):

    product = Product.objects.get(id=id)
    product.delete()
    return redirect('all_product')

    return render(request, 'ecommerce/stuff_page/product_table.html',)

@staff_member_required
def product_edit(request, id):

    product = Product.objects.get(id=id)

    product_type = Product_type.objects.all().order_by('-id')

    if request.method == 'POST' and 'product_edit' in request.POST:
        product.name = request.POST.get('product_name').strip()
        product.price =  request.POST.get('product_price').strip()
        product.product_type = request.POST.get('product_type').strip()
        product.discription = request.POST.get('product_dis').strip()
        product.digital = request.POST.get('product_status')

        if 'product_img' in request.FILES:
            img_path =  os.path.join(MEDIA_DIR,product.image.name)
            delete_old_img = True
            product.image = request.FILES.get('product_img')
        
        product.save()
        return redirect('all_product')
    
    try:
        if delete_old_img:
            os.remove(img_path)
    except:
        pass 

    context = {
        'product' : product,
        'product_type' : product_type,
    }

    return render(request, 'ecommerce/stuff_page/product_edit.html', context)

@staff_member_required
def order_table(request):

    order_check_search = False

    order = Order.objects.all().order_by('-id')
    paginator = Paginator(order, 5)  # Show 5 obj per page

    page = request.GET.get('page')
    order = paginator.get_page(page)

    if request.method == 'POST' and 'order_search_btn' in request.POST:
        
        q = request.POST.get('order_search').strip()

        order = Order.objects.filter(order_id__exact=q)
        order_check_search = True

    context = {
        'order' : order,
        'order_check_search' : order_check_search,
    }

    return render(request, 'ecommerce/stuff_page/order_table.html', context)

@staff_member_required
def order_details(request, id):

    order = Order.objects.get(id=id)
    order_item = OrderItem.objects.filter(order=order).order_by('quantity')
    shipping = ShippingAddress.objects.get(order=order)
    paymt = payment.objects.get(order=order)
 
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

@login_required
def user_order(request):

    product_type = Product_type.objects.all().order_by('-id')

    check_search = False

    data = cartData(request)
    cartItems = data['cartItems']

    order_count = Order.objects.filter(customer=request.user).count()

    order = Order.objects.filter(customer=request.user).order_by('-id')
    order_item = OrderItem.objects.filter(order__customer=request.user).order_by('quantity')
    
    paginator = Paginator(order, 4)  # Show 4 obj per page
    page = request.GET.get('page')
    order = paginator.get_page(page)

    if request.method == 'POST' and 'user_order_btn' in request.POST:
        q = request.POST.get('user_order_search').strip()

        criterion1 = Q(customer__exact=request.user)
        criterion2 = Q(order_id=q)

        order = Order.objects.filter(criterion1 & criterion2)
        check_search = True
  
    

    context = {
        'order' : order,
        'order_item' : order_item,
        'order_count' : order_count,
        'check_search' : check_search,

        'cartItems' : cartItems,
        'product_type' : product_type,
    }

    return render(request, 'ecommerce/user_order.html', context)