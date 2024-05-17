from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as UCreationF
from django.contrib.auth.forms import UserChangeForm as UChangeF

User = get_user_model()


class UserCreationForm(UCreationF):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class UserChangeForm(UChangeF):
    class Meta:
        model = User
        fields = "__all__"
