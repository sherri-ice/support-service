from rest_framework import serializers
from .models import Ticket
from django.utils.translation import gettext_lazy as _


class AbstractTicketSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate(data):
        status = data.get('status', None)
        if status and status not in Ticket.Statuses:
            raise serializers.ValidationError(
                {'status': _(f'Invalid status: {status}')},
                code='invalid',
            )
        return data

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class AdminTicketSerializer(AbstractTicketSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'body_text', 'owner', 'status']
        read_only_fields = ['id', 'owner']


class CommonUserTicketSerializer(AbstractTicketSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'body_text', 'owner', 'status']
        read_only_fields = ['id', 'owner', 'status']
