from django.urls import path
from .views import ChangePasswordView, LoginView, RefreshTokenView, RegisterView


app_name = "authentication"


urlpatterns = [
    path("change-password", ChangePasswordView.as_view(), name="change-password"),
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register-user"),
    path("refresh-token", RefreshTokenView.as_view(), name="refresh-token"),
]
