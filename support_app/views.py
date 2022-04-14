from rest_framework import generics
from .models import Ticket, Message
from .serializers import AdminTicketSerializer, CommonUserTicketSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated


class RetrieveUpdateDestroyTicketAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff:
            return AdminTicketSerializer
        return CommonUserTicketSerializer


class ListCreateTicketAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommonUserTicketSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(owner=user)
