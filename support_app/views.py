from rest_framework import generics
from .models import Ticket
from .serialisers import TicketSerializer


class TicketListAPIView(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
