from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    text = serializers.CharField()
    media_url = serializers.URLField()
    send_date = serializers.DateTimeField(read_only=True)
    ticket = serializers.ReadOnlyField(source='ticket.id')

    class Meta:
        model = Message
        fields = ('id', 'send_date', 'ticket', 'text', 'media_url')
