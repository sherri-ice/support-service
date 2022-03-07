from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serialisers import RegistrationSerializer

from .models import User


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

