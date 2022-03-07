from rest_framework import serializers

from user_handler_app.models import User
from .models import Ticket
from django.utils.translation import gettext_lazy as _


class TicketSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField()
    body_text = serializers.CharField()
    status = serializers.CharField()
    creation_date = serializers.DateTimeField(read_only=True)
    last_edited_date = serializers.DateTimeField(read_only=True)
    media_url = serializers.URLField(allow_null=True, required=False)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                               default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = '__all__'

    def validate(self, data):
        status = data.get('status', None)
        if status not in Ticket.Statuses:
            raise serializers.ValidationError(
                {'status': _(f'Invalid status: {status}')},
                code='invalid',
            )

        return data

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
