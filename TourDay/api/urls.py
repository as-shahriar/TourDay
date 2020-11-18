from django.urls import path, include
from api import auth, profile, views, event
from _auth.views import forgetPasswordView, resetPasswordView
from user_profile.views import PostList, delete_account
from django.views.generic import TemplateView
from event.views import AllEventList, pay, dashboard, edit_event

urlpatterns = [
    path('', TemplateView.as_view(template_name="api/doc.html"), name="api_doc"),

    # Auth
    path('auth/', include('rest_auth.urls')),
    path('auth/signup/', auth.Signup.as_view()),
    path('forget_password/', forgetPasswordView),
    path('reset_password/<str:slug>/', resetPasswordView),
    path('delete_account/', delete_account),

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
    path("event-pay/<int:id>", pay),
    path('create_event/', dashboard),
    path('edit_event/<int:id>', edit_event),
    path('going_users/<str:id>', event.GoingUser.as_view()),

    path('search/user/<str:q>', views.SearchUser.as_view()),
    path('search/product/<str:q>', views.SearchProduct.as_view()),
    path('map/<str:username>', views.map),

]
