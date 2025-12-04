from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    Register a new user.

    Creates a new user account with username, email, and password. Email must be unique.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
