from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .models import Ticket
from .serialisers import TicketSerializer
from .permissions import IsOwner
from rest_framework.permissions import AllowAny, IsAdminUser


class TicketListAPIView(ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser, ]


class TicketAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    # permission_classes = [IsAdminUser, IsOwner]
    permission_classes = [AllowAny, ]
