from event.views import EventList
from django.shortcuts import get_object_or_404
from event.serializer import EventSerializer
from event.models import Event, Transactions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from _auth.models import User
from user_profile.models import Profile
from .serializer import ProfileSerializer
from rest_framework.response import Response
from utils import async_send_mail
from TourDay.settings import EMAIL_HOST_USER
from django.db.models import Q


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
        data = ProfileSerializer(data=going, many=True)
        data.is_valid()
        return Response(data.data)


class Pay(APIView):
    def post(self, request, *args, **kwargs):
        method = request.POST.get("method")
        tr = request.POST.get("tr")
        id = kwargs.get('id')

        try:
            # if True:
            event = Event.objects.get(id=id)
            if Transactions.objects.filter(
                Q(event=event), Q(user=request.user)
            ).count() != 0:
                raise ValueError
            obj = Transactions()
            obj.event = event
            obj.method = method.strip()
            obj.tr = tr.strip()
            obj.user = request.user
            obj.save()
            event.pending.add(request.user)
            event.save()
            subject = f"New payment request for {event.title} | {request.user.username}"
            message = f"Dear {event.host.username},\nYour event '{event.title}' in TourDay gets a new payment request. Kindly review the request on https://tourday.team/event/{event.id}\nBest Regards\nTourDay Team"
            async_send_mail(subject, message,
                            EMAIL_HOST_USER, event.host.email)
            return Response({"status": 200})
        except:
            pass
        return Response({"status": 400})


class CreateEvent(APIView):
    def post(self, request):
        try:
            event = Event()
            event.host = request.user
            event.title = request.POST.get('title')
            event.location = request.POST.get('location')
            event.date = request.POST.get('date')
            event.details = request.POST.get('details')
            event.capacity = request.POST.get('capacity')
            event.pay1 = request.POST.get('pay1')
            event.pay2 = request.POST.get('pay2')
            event.cost = request.POST.get('cost')
            event.pay1_method = request.POST.get('pay1_method')
            event.pay2_method = request.POST.get('pay2_method')
            event.save()
            event.going.add(request.user)
            return Response({'status': 200, "id": event.id})
        except:
            return Response({'status': 400})


class EditEvent(APIView):
    def post(self, request, *args, **kwargs):
        id = kwargs.get('id')
        event = Event.objects.get(id=id)
        if request.user == event.host:
            event.title = request.POST.get('title').title()
            event.location = request.POST.get('location')
            event.date = request.POST.get('date')
            event.details = request.POST.get('details')
            event.capacity = request.POST.get('capacity')
            event.pay1 = request.POST.get('pay1')
            event.pay2 = request.POST.get('pay2')
            event.cost = request.POST.get('cost')
            event.pay1_method = request.POST.get('pay1_method')
            event.pay2_method = request.POST.get('pay2_method')
            if request.FILES.get("image") != None:
                event.image = request.FILES.get("image")
            event.save()
            return Response({'status': 200, "id": event.id})
        return Response({'status': 400})
