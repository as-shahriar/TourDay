from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ecommerce.models import Product
from ecommerce.serializers import ProductSerializer

@api_view(['GET',])
def product_details(request, id):

    try:
        product_details = Product.objects.get(id=id)
        serializer = ProductSerializer(product_details, many=False)
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)  # Not found

    
