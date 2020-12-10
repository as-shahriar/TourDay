from rest_framework import serializers
from .models import Product, Order, OrderItem, ShippingAddress, Product_type

class ProductSerializer(serializers.ModelSerializer):

	class Meta:
		model = Product
		fields =['id', 'name', 'price', 'product_type', 'digital', 'image', 'description']

#End here

class orderItemdetails(serializers.ModelSerializer):
	
	class Meta:
		model = OrderItem
		fields = ['quantity']

class orderdetails(serializers.ModelSerializer):
	
	class Meta:
		model = Order
		fields = ['id', 'date_ordered', 'total_money', 'total_items', 'status', 'order_id']

class orderProduct(serializers.ModelSerializer):

	class Meta:
		model = Product
		fields = ['id', 'name' , 'price', 'image']



class orderitemSerializer(serializers.ModelSerializer):
	
	# product = serializers.ReadOnlyField(source='product.name')
	product = orderProduct(many=False, read_only=True)
	order = orderdetails(many=False, read_only=True)
	
	class Meta:
		model =  OrderItem
		fields = ['id', 'quantity', 'product', 'order']


class Product_typeSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Product_type
		fields = '__all__'