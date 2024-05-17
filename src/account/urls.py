from django.urls import path
from .views import UserListView, UserDetailsView


app_name = "account"


urlpatterns = [
    path("users", UserListView.as_view(), name="user-list"),
    path("me", UserDetailsView.as_view(), name="user-details"),
]
