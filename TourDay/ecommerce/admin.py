from django.contrib import admin

# Register your models here.
from .models import *

class list_OrderItem(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'date_added')

class list_Product(admin.ModelAdmin):
    list_display = ('name', 'price')

class list_Order(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_money', 'total_items', 'status', 'order_id', 'date_ordered')


admin.site.register(Product, list_Product)
admin.site.register(Order, list_Order)
admin.site.register(OrderItem, list_OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(payment)
admin.site.register(Product_type)