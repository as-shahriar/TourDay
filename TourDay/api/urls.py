from django.urls import path, include
from api import auth, profile, views, event
from _auth.views import forgetPasswordView, resetPasswordView
from user_profile.views import PostList
from django.views.generic import TemplateView
from event.views import AllEventList

urlpatterns = [
    path('', TemplateView.as_view(template_name="api/doc.html"), name="api_doc"),

    # Auth
    path('auth/', include('rest_auth.urls')),
    path('auth/signup/', auth.Signup.as_view()),
    path('forget_password/', forgetPasswordView),
    path('reset_password/<str:slug>/', resetPasswordView),
    path('delete_account/', auth.DeleteAccount.as_view()),

    # Profile
    path('profile/', profile.ProfileView.as_view()),
    path('get_posts/<str:username>', PostList.as_view()),
    path('post/', profile.PostWrite.as_view()),
    path('post_delete/', profile.PostDelete.as_view()),
    path('user/<int:id>', profile.UserDetailsByID.as_view()),
    path('user/<str:username>', profile.UserDetails.as_view()),

    path('post/like/', profile.LikePost.as_view()),

    # Event
    path('get_events/<str:username>', event.EventListApi.as_view()),
    path('all-events/', AllEventList.as_view()),
    path('going-events/<str:username>', event.GoingEventList.as_view()),
    path("event-pay/<int:id>", event.Pay.as_view()),
    path('create_event/', event.CreateEvent.as_view()),
    path('edit_event/<int:id>', event.EditEvent.as_view()),
    path('going_users/<int:id>', event.GoingUser.as_view()),
    path('event/<int:id>', event.EventView.as_view()),
    path('event/transactions/<int:id>', event.EventTransaction.as_view()),
    path('event/transactions/action/<int:id>',
         event.EventTransactionHandler.as_view()),

    path('search/user/<str:q>', views.SearchUser.as_view()),
    path('search/product/<str:q>', views.SearchProduct.as_view()),
    path('search/event/<str:q>', views.SearchEvent.as_view()),
    path('map/<str:username>', views.map),
    path('map-dark/<str:username>', views.map_dark),

]
