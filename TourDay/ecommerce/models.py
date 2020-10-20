from django.db import models
from django.contrib.auth.models import User
from user_profile.models import Profile
import datetime
# Create your models here.

STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Shipping", "Shipping"),
    ("Shipped", "Shipped"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled"),
    ("Returned", "Returned"),
    ("PaymentError", "PaymentError"),
)


class Product(models.Model):
    name = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    product_type = models.CharField(max_length=20, null=True, blank=True)
    price = models.IntegerField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(upload_to='ecom_pics', blank=False)
    in_stock = models.BooleanField(default=True, null=True, blank=True)

    def save(self):
        super().save()

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateField(default=datetime.date.today)
    complete = models.BooleanField(default=False)

    total_money = models.IntegerField(default=0, null=True, blank=True)
    total_items = models.IntegerField(default=0, null=True, blank=True)
    status = models.CharField(
        max_length=30, null=True, blank=True, choices=STATUS_CHOICES, default="Pending")
    order_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.order_id

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateField(default=datetime.date.today)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    PhoneNo = models.CharField(max_length=50, null=False, blank=True)
    allPhoneNo = models.CharField(max_length=50, null=False, blank=True)
    address = models.CharField(max_length=200, null=False, blank=True)
    city = models.CharField(max_length=200, null=False, blank=True)
    state = models.CharField(max_length=200, null=False, blank=True)
    zipcode = models.CharField(max_length=200, null=False, blank=True)
    date_added = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.address


class payment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    method = models.CharField(max_length=50, null=True, blank=True)

    payment_method = models.CharField(max_length=50, null=True, blank=True)
    PhoneNo = models.CharField(max_length=50, null=False, blank=True)
    trxId = models.CharField(max_length=50, null=False, blank=True)

    def __str__(self):
        return str(self.customer)


class Product_type(models.Model):
    product_type = models.CharField(max_length=50, null=False, blank=True)

    def __str__(self):
        return self.product_type
