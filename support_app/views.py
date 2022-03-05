from django.shortcuts import render
from rest_framework import generics
from .models import Message
from .serialisers import MessageSerializer


class MessageListApiView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
