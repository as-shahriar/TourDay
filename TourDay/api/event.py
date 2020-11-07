from event.views import EventList
from django.shortcuts import get_object_or_404
from event.serializer import EventSerializer
from event.models import Event
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from _auth.models import User
from user_profile.models import Profile
from .serializer import ProfileSerializer
from rest_framework.response import Response

class EventListApi(EventList):
    permission_classes = [IsAuthenticated]

class GoingEventList(APIView, LimitOffsetPagination):
    permission_classes = [AllowAny]
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(User, username=username)
        instance = Event.objects.filter(going__in=[user]).order_by("-date")
        # instance = Event.objects.all()
        instance = self.paginate_queryset(instance, request, view=self)
        serializer = self.serializer_class(instance, many=True)
        return self.get_paginated_response(serializer.data)

class GoingUser(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        event = get_object_or_404(Event, id=id)
        going = Profile.objects.filter(user__in=event.going.all())
        data = ProfileSerializer(data=going,many=True)
        data.is_valid()
        return Response(data.data)