from rest_framework import generics
from .models import Ticket
from .serialisers import TicketSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated


class TicketListAPIView(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser, ]


class TicketAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsOwnerOrAdmin]


class TicketAPICreateView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]


