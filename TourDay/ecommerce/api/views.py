from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ecommerce.models import Product, Order, OrderItem, ShippingAddress,Product_type
from ecommerce.serializers import ProductSerializer, orderitemSerializer, Product_typeSerializer
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework import generics

@api_view(['GET',])
def product_details(request, id):

    try:
        product_details = Product.objects.get(id=id)
        serializer = ProductSerializer(product_details, many=False)
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)  # Not found


@api_view(['GET',])   
@permission_classes((IsAuthenticated,))
def order_details(request):

    paginator = PageNumberPagination()
    paginator.page_size = 4

    try:
        order_details = OrderItem.objects.filter(order__customer=request.user).order_by('-id')
        order_details = paginator.paginate_queryset(order_details, request)
        serializer = orderitemSerializer(order_details, many=True)
        return paginator.get_paginated_response(serializer.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)  # bad request



@api_view(['GET', ])
def product_home(request):

    paginator = PageNumberPagination()
    paginator.page_size = 15

    try:
        product = Product.objects.all().order_by('-id')
        product = paginator.paginate_queryset(product, request)
        serializer = ProductSerializer(product, many=True)
        return paginator.get_paginated_response(serializer.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)  # bad request

@api_view(['GET', ])
def all_category(request):

    try:
        product_type = Product_type.objects.all().order_by('-id')
        serializer = Product_typeSerializer(product_type, many=True)
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)  # bad request


@api_view(['GET', ])
def category_product(request, slug):

    paginator = PageNumberPagination()
    paginator.page_size = 15

    try:
        category_product = Product.objects.filter(product_type=slug)
        category_product = paginator.paginate_queryset(category_product, request)
        serializer = ProductSerializer(category_product, many=True)
        return paginator.get_paginated_response(serializer.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)  # bad request


class SetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 10000

class search_product(generics.ListAPIView):
    
    queryset = Product.objects.all().order_by('-id')
    pagination_class = SetPagination
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'product_type'] 
    