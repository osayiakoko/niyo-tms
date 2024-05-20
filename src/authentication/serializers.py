from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User
from core.exceptions import APIException


class JwtTokenSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    token = JwtTokenSerializer(read_only=True)

    def validate_password(self, value):
        if len(value) < 8:
            raise APIException(detail="Password must be at least 8 characters long.")

        if not any(char.isupper() for char in value):
            raise APIException(
                detail="Password must contain at least one uppercase letter."
            )

        if not any(char.isdigit() for char in value):
            raise APIException(detail="Password must contain at least one number.")

        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        update_last_login(None, user)
        return user


class LoginSerializer(serializers.Serializer):
    """'
    Login Serializer
    """

    email = serializers.EmailField()
    password = serializers.CharField()


class UserTokenSerializer(serializers.ModelSerializer):
    token = JwtTokenSerializer(read_only=True)

    class Meta:
        model = User

        read_only_fields = ["id", "token"]

        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "token",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        old_password = attrs["old_password"]
        new_password = attrs["new_password"]

        # Check old password
        user: User = self.context["request"].user
        if not user.check_password(old_password):
            raise APIException(detail="Invalid old password")

        # check if passwords are different
        if old_password == new_password:
            raise APIException(detail="New password same as old")

        return super().validate(attrs)


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True)
    access_token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        refresh_token = RefreshToken(attrs["refresh_token"])

        data = {"access_token": str(refresh_token.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh_token
                    refresh_token.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh_token.set_jti()
            refresh_token.set_exp()

            data["refresh_token"] = str(refresh_token)

        return data
