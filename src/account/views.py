from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializers import UserSerializer
from .models import User


class UserDetailsView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
