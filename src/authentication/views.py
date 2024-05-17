from django.contrib import auth
from django.contrib.auth.models import update_last_login
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from authentication.serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
    RegisterSerializer,
    UserTokenSerializer,
)


class RegisterView(GenericAPIView):
    """Endpoint for registering users"""

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    """
    An endpoint for user login.
    """

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @extend_schema(responses={200: UserTokenSerializer})
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data.get("email")
        password = serializer.data.get("password")
        user = auth.authenticate(username=str(username), password=password)

        if user and user.is_active:
            serializer = UserTokenSerializer(user)
            update_last_login(None, user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(GenericAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer

    @extend_schema(responses={200: str})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        # set_password also hashes the password that the user will get
        user = request.user
        user.set_password(serializer.data.get("new_password"))
        user.save()

        return Response("Password updated successfully", status=status.HTTP_200_OK)


class RefreshTokenView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    permission_classes = [AllowAny]

    serializer_class = RefreshTokenSerializer
