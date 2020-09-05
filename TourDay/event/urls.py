from django.urls import path
from event import views
urlpatterns = [
    path("dashboard/", views.dashboard, name="event_dashboard"),
    path("<int:id>", views.eventView, name="event_page")

]
