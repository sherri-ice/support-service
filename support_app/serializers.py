from rest_framework import serializers
from .models import Ticket, Message
from django.utils.translation import gettext_lazy as _


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text']
        read_only_fields = ['send_date']


class AbstractTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        messages = MessageSerializer(many=True)

    def validate(self, attrs):
        status = attrs.get('status', None)
        if status and status not in Ticket.Statuses:
            raise serializers.ValidationError(
                {'status': _(f'Invalid status: {status}')},
                code='invalid',
            )
        return super().validate(attrs)

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class AdminTicketSerializer(AbstractTicketSerializer):
    messages = MessageSerializer(many=True, source="ticket_messages",
                                 read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'body_text', 'owner', 'status', 'messages']
        extra_kwargs = {"owner": {"required": False, "allow_null": True}}


class CommonUserTicketSerializer(AbstractTicketSerializer):
    messages = MessageSerializer(many=True, source="ticket_messages",
                                 read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'body_text', 'owner', 'status', 'messages']
        extra_kwargs = {"owner": {"required": False, "allow_null": True}}
