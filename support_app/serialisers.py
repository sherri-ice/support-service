from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField()
    body_text = serializers.CharField()
    status = serializers.CharField()
    creation_date = serializers.DateTimeField(read_only=True)
    last_edited_date = serializers.DateTimeField(read_only=True)
    media_url = serializers.URLField()
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Ticket
        fields = '__all__'
