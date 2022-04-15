from rest_framework import generics

from .models import Ticket
from .serializers import AdminTicketSerializer, CommonUserTicketSerializer, \
    MessageSerializer
from .permissions import AdminOrOwnerReadOnly
from rest_framework.permissions import IsAuthenticated

from .tasks import send_email

from .utils import EmailType


class RetrieveUpdateDestroyTicketAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    permission_classes = [AdminOrOwnerReadOnly]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff:
            return AdminTicketSerializer
        return CommonUserTicketSerializer

    def patch(self, request, *args, **kwargs):
        if 'status' in request.data:
            ticket = Ticket.objects.get(id=self.kwargs['pk'])
            send_email.delay(EmailType.TICKET_STATUS_UPDATE, ticket.owner.email,
                             ticket.id,
                             ticket.status)
        return super().patch(request, *args, **kwargs)


class ListCreateTicketAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommonUserTicketSerializer

    def perform_create(self, serializer):
        ticket = serializer.save(owner=self.request.user)
        send_email.delay(EmailType.TICKET_CREATION, ticket.owner.email,
                         ticket.id, ticket.body_text)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(owner=user)


class AddMessageToTicketAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        ticket = Ticket.objects.get(id=self.kwargs['pk'])
        message = serializer.save(owner=self.request.user, ticket=ticket)
        if self.request.user != ticket.owner:
            send_email.delay(EmailType.TICKET_NEW_MESSAGE, ticket.owner.email,
                             ticket.id, message.text)
