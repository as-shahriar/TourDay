from event.views import EventList
from django.shortcuts import get_object_or_404
from event.serializer import EventSerializer
from event.models import Event, Transactions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from _auth.models import User
from user_profile.models import Profile
from .serializer import ProfileSerializer, TransactionSerializer
from rest_framework.response import Response
from utils import async_send_mail
from TourDay.settings import EMAIL_HOST_USER
from django.db.models import Q
from rest_framework import status


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
                return Response({'message': 'Pendinng payment exists'}, status=status.HTTP_403_FORBIDDEN)
            transaction = Transactions.objects.filter(
                Q(user__in=event.pending.all()), Q(
                    status=False), Q(event=event)
            )
            if event.capacity <= event.going.count() + transaction.count():
                return Response({'message': 'Sorry housefull'}, status=status.HTTP_403_FORBIDDEN)

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


class EventView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        event = get_object_or_404(Event, id=id)
        serializer = EventSerializer(event, many=False)
        # print(serializer.data)
        return Response(serializer.data)


class EventTransaction(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        event = get_object_or_404(Event, id=id)
        if request.user != event.host:
            return Response({'message': 'No access'}, status=status.HTTP_403_FORBIDDEN)
        transaction = Transactions.objects.filter(
            Q(user__in=event.pending.all()), Q(status=False), Q(event=event)
        )
        serializer = TransactionSerializer(transaction, many=True)
        # print(serializer.data)
        return Response(serializer.data)


class EventTransactionHandler(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event_id = kwargs.get('id')
        tr_id = request.POST.get('tr_id')
        is_accepted = request.POST.get('action')
        user_id = request.POST.get("user_id")

        event = get_object_or_404(Event, id=event_id)
        user = User.objects.get(id=user_id)
        tr = Transactions.objects.filter(
            Q(user=user), Q(event=event)
        )
        if request.user != event.host:
            return Response({'message': 'No access'}, status=status.HTTP_403_FORBIDDEN)

        if is_accepted == "1":
            event.going.add(user)
            event.pending.remove(user)
            tr.status = True
            tr.update()
            profile = Profile.objects.get(user=user)
            subject = f"Payment request accepted for {event.title}."
            message = f"Dear {user.username},\nYour payment request for event '{event.title}' in TourDay got accepted. Pack your bags and get ready to explore!\nKeep eye on https://tourday.team/event/{event.id}\nBest Regards\nTourDay Team"
            async_send_mail(subject, message,
                            EMAIL_HOST_USER, user.email)
            return Response({"message": "Transaction accepted"}, status=status.HTTP_202_ACCEPTED)
        elif is_accepted == "0":
            event.pending.remove(user)
            tr.delete()
            subject = f"Payment request denied for {event.title}."
            message = f"Dear {user.username},\nYour payment request for event '{event.title}' in TourDay got denied. Kindly check your transaction number and try again.\nBest Regards\nTourDay Team"
            async_send_mail(subject, message,
                            EMAIL_HOST_USER, user.email)
            return Response({"message": "Transaction isn't accepted"}, status=status.HTTP_200_OK)


class EventDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        id = kwargs.get('id')
        event = get_object_or_404(Event, id=id)
        if request.user != event.host:
            return Response({'message': 'No access'}, status=status.HTTP_403_FORBIDDEN)
        event.delete()
        return Response({"message": "Event deleted."}, status=status.HTTP_200_OK)
