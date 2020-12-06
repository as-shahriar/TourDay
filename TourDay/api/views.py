from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import ProfileSerializer, EventSerializer
from user_profile.models import Profile
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination
from ecommerce.models import Product
from ecommerce.serializers import ProductSerializer
from event.models import Event


def map(request, username):
    return render(request, 'api/map.html', {'username': username})


def map_dark(request, username):
    return render(request, 'api/map-dark.html', {'username': username})


class SearchUser(APIView, LimitOffsetPagination):
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        q = kwargs.get('q')
        queries = q.split(" ")
        instance = None
        for query in queries:
            if instance:
                instance |= Profile.objects.filter(
                    Q(name__icontains=query) | Q(
                        email__icontains=query) | Q(city__icontains=query)
                )
            else:
                instance = Profile.objects.filter(
                    Q(name__icontains=query) | Q(
                        email__icontains=query) | Q(city__icontains=query)
                )
        instance = self.paginate_queryset(instance, request, view=self)

        serializer = self.serializer_class(instance, many=True)

        return self.get_paginated_response(serializer.data)


class SearchProduct(APIView, LimitOffsetPagination):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        q = kwargs.get('q')
        queries = q.split(" ")
        instance = None
        for query in queries:
            if instance:
                instance |= Product.objects.filter(
                    Q(name__icontains=query) | Q(description__icontains=query) | Q(
                        product_type__icontains=query)
                )
            else:
                instance = Product.objects.filter(
                    Q(name__icontains=query) | Q(description__icontains=query) | Q(
                        product_type__icontains=query)
                )
        instance = self.paginate_queryset(instance, request, view=self)

        serializer = self.serializer_class(instance, many=True)

        return self.get_paginated_response(serializer.data)


class SearchEvent(APIView, LimitOffsetPagination):
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        q = kwargs.get('q')
        queries = q.split(" ")
        instance = None
        for query in queries:
            if instance:
                instance |= Event.objects.filter(
                    Q(title__icontains=query) | Q(location__icontains=query) | Q(
                        details__icontains=query)
                )
            else:
                instance = Event.objects.filter(
                    Q(title__icontains=query) | Q(location__icontains=query) | Q(
                        details__icontains=query)
                )
        instance = self.paginate_queryset(instance, request, view=self)

        serializer = self.serializer_class(instance, many=True)

        return self.get_paginated_response(serializer.data)
