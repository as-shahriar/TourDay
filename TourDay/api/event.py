from event.views import EventList
from rest_framework.permissions import IsAuthenticated


class EventListApi(EventList):
    permission_classes = [IsAuthenticated]
