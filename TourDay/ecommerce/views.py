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

#email
from utils import async_send_mail
from TourDay.settings import EMAIL_HOST_USER

# generate pdf
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa



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
    paginator = Paginator(products, 15)  # Show 15 obj per page

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

            #email here
            email = request.user.email
            subject = "We've received your order, check to see if everything is OK before confirming"
            message = f"Dear {profile.name},\nWe've received your order. Order ID {ord.order_id}. You have ordered a total of {ord.total_items} products which cost BDT. {ord.total_money}. \n\n\nCongratulations on your prudence in ordering products online. With this decision you are saving your precious few hours which would have been spent on street jams, shopping in stores. We know the value of your time. So we will try to deliver the products to you as soon as possible. Our work on your order will start right now. We will approve your order shortly. You will receive a confirmation message via email/phone. We will then provide the courier service to get your parcel ready and sent as soon as possible and at the same time confirm you via email. So check the email inbox to stay updated about your order status.\n\nGood luck always,\nTourDay Team!" 
            async_send_mail(subject, message, EMAIL_HOST_USER, email)

            return redirect('checkout_message')
        
    
    shipping_add = ShippingAddress.objects.all()

    shipping_check = False
    shipping_check = ShippingAddress.objects.filter(customer=request.user).order_by('-id').exists()
    
    if shipping_check:
        shipping_add = ShippingAddress.objects.filter(customer=request.user).order_by('-id')[0]

    context = {
    'items':items,
    'order':order,
    'cartItems':cartItems,
    'profile' : profile,
    'product_type' : product_type,

    'shipping_check' : shipping_check,
    'shipping_add' : shipping_add,   
    
    }
    return render(request, 'ecommerce/checkout.html', context)

@staff_member_required
def staff_pages(request):

    return render(request, 'ecommerce/stuff_page/main.html')

@staff_member_required
def product_table(request):

    product_check_search = False

    product = Product.objects.all().order_by('-id')
    
    paginator = Paginator(product, 25)  # Show 25 obj per page

    page = request.GET.get('page')
    product = paginator.get_page(page)

    if request.method == 'POST' and 'btn_product_search' in request.POST:
        
        q = request.POST.get('product_search').strip()
        product = Product.objects.filter(Q(name__icontains=q) | Q(product_type__icontains=q))

        product_check_search = True

    context = {
        'product' : product,
        'product_check_search' : product_check_search,
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
        product.description = request.POST.get('product_dis').strip()
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
        product.description = request.POST.get('product_dis').strip()
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
    paginator = Paginator(order, 25)  # Show 25 obj per page

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

    profile = get_object_or_404(Profile, user=request.user)

    order = Order.objects.get(id=id)
    order_item = OrderItem.objects.filter(order=order).order_by('quantity')
    shipping = ShippingAddress.objects.get(order=order)
    paymt = payment.objects.get(order=order)
 
    if request.method == 'POST' and 'order_submit' in request.POST:
        order.status = request.POST.get('payment_mtd')
        order.save()
        
         #email here
        email = request.user.email
        if order.status == "Approved":
            subject = f"Your order has been approved. Please match again."
            message = f"Dear {profile.name}, \nYour order has been approved. Your order ID is {order.order_id}.\n\nWe have started working on your order. We will deliver your product very quickly.\nHowever, for some reason, despite our sincere desire and effort, we are not able to deliver the product faster. Because of the weekly closure of product collection locations, it may take some time for us to collect products out of stock. Even then we will try our best to deliver your order as soon as possible.\nWe hope that your ordered products will be delivered to you soon.\n\nGood luck always.\nTourDay Team."
            async_send_mail(subject, message, EMAIL_HOST_USER, email)

        if order.status == "Shipped":

            subject = f"Your order has been shipped.Take a look at the details"
            message = f"Dear {profile.name}, \nYour order (ID {order.order_id}) has been prepared by us and sent to the delivery team. Your parcel is ready with utmost importance. Hope to receive your parcel very soon.We hope to receive your parcel in a few days. In case of delay in delivery, please contact tourday.bd@gmail.com via email.\n\nWe hope that your ordered products will be delivered to you soon.\n\nGood luck always.\nTourDay Team."
            async_send_mail(subject, message, EMAIL_HOST_USER, email)
        
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


@login_required
def checkout_message(request):

    data = cartData(request)
    cartItems = data['cartItems']

    product_type = Product_type.objects.all().order_by('-id')
    order = Order.objects.filter(customer=request.user).order_by('-id')[0]

    context = {
        'cartItems' : cartItems,
        'order' : order,
        'product_type' : product_type,
    }

    return render(request, 'ecommerce/order_con.html', context)



    #Generated pdf
def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None



#Opens up page as PDF
class ViewPDF(View):
    def get(self, request, *args, **kwargs):

        order = Order.objects.filter(customer=request.user).order_by('-id')[0]
        shipping = ShippingAddress.objects.filter(customer=request.user).order_by('-id')[0]
        pay = payment.objects.filter(customer=request.user).order_by('-id')[0]

        oder_items = OrderItem.objects.filter(order__order_id=order.order_id)

        data = {
            'order' : order,
            'shipping' : shipping,
            'payment' : pay,
            'oder_items' : oder_items,
        }

        pdf = render_to_pdf('ecommerce/pdf/pdf_view.html', data)
        return HttpResponse(pdf, content_type='application/pdf')




# # Automaticly downloads to PDF file
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):

        order = Order.objects.filter(customer=request.user).order_by('-id')[0]
        shipping = ShippingAddress.objects.filter(customer=request.user).order_by('-id')[0]
        pay = payment.objects.filter(customer=request.user).order_by('-id')[0]

        oder_items = OrderItem.objects.filter(order__order_id=order.order_id)

        data = {
            'order' : order,
            'shipping' : shipping,
            'payment' : pay,
            'oder_items' : oder_items,
        }

        pdf = render_to_pdf('ecommerce/pdf/pdf_view.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" %(order.order_id)
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response


def Category_items(request, slug):


    data = cartData(request)

    cartItems = data['cartItems']

    product_type = Product_type.objects.all().order_by('-id')
    
    products = Product.objects.filter(product_type=slug).order_by('-id')
    paginator = Paginator(products, 15)  # Show 15 obj per page

    page = request.GET.get('page')
    products = paginator.get_page(page)


    context = {

        'product_type' :  product_type,
        'products':products, 
        'cartItems':cartItems,
    }


    return render(request, 'ecommerce/category_items.html', context)


def search_items(request):


    data = cartData(request)

    cartItems = data['cartItems']

    product_type = Product_type.objects.all().order_by('-id')
    
    q = request.GET.get('q')
    if q == None:
        return redirect("all_product")
    products = Product.objects.all().filter(
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(product_type__icontains=q))


    paginator = Paginator(products, 15)  # Show 15 obj per page

    page = request.GET.get('page')
    products = paginator.get_page(page)


    context = {

        'product_type' :  product_type,
        'products':products, 
        'cartItems':cartItems,
    }


    return render(request, 'ecommerce/search_items.html', context)

