from django.urls import path
from event import views


urlpatterns = [
    path("dashboard/", views.dashboard, name="event_dashboard"),
    path("<int:id>", views.eventView, name="event_page"),
    path("get_events/<str:username>", views.EventList.as_view()),
    path("edit_events/<int:id>", views.edit_event),
    path("action/<int:id>", views.action),
    path("pay/<int:id>", views.pay),
    path("delete/<int:id>", views.delete_event),
    path("all/",views.all,name="all_event"),
    path("all-events/", views.AllEventList.as_view()),
    

]
