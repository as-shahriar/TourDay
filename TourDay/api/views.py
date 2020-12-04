from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import ProfileSerializer
from user_profile.models import Profile
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination
from ecommerce.models import Product
from ecommerce.serializers import ProductSerializer


def map(request, username):
    return render(request, 'api/map.html', {'username': username})


def map_dark(request, username):
    return render(request, 'api/map-dark.html', {'username': username})


class SearchUser(APIView, LimitOffsetPagination):
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        q = kwargs.get('q')

        instance = Profile.objects.filter(

            Q(name__icontains=q) | Q(email__icontains=q) | Q(city__icontains=q)
        )
        instance = self.paginate_queryset(instance, request, view=self)

        serializer = self.serializer_class(instance, many=True)

        return self.get_paginated_response(serializer.data)


class SearchProduct(APIView, LimitOffsetPagination):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        q = kwargs.get('q')

        instance = Product.objects.filter(

            Q(name__icontains=q) | Q(description__icontains=q) | Q(
                product_type__icontains=q)
        )
        instance = self.paginate_queryset(instance, request, view=self)

        serializer = self.serializer_class(instance, many=True)

        return self.get_paginated_response(serializer.data)
