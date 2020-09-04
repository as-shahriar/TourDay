from django.urls import path
from event import views
urlpatterns = [
    path("dashboard/", views.dashboard, name="event_dashboard")

]
