from django.urls import path
from event import views
urlpatterns = [
    path("dashboard/", views.dashboard, name="event_dashboard"),
    path("<int:id>", views.eventView, name="event_page"),
    path("get_events/", views.EventList.as_view()),
    path("edit_events/<int:id>", views.edit_event)

]
