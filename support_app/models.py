from django.db import models


class Message(models.Model):
    text = models.TextField()
    media_url = models.URLField(blank=True)
    send_date = models.DateTimeField(auto_now_add=True)
    ticket_id = models.ForeignKey('Ticket', related_name="messages",
                                  on_delete=models.CASCADE)
    # owner_id


class Ticket(models.Model):
    class Status:
        ACTIVE = 1
        FROZEN = 2
        CLOSED = 3
        STATUS_CHOICES = (
            (ACTIVE, 'Active'),
            (FROZEN, 'Frozen'),
            (CLOSED, 'Closed'),
        )

    title = models.CharField(max_length=255)
    body_text = models.TextField()
    media_url = models.URLField(blank=True)
    status = models.IntegerField(choices=Status.STATUS_CHOICES,
                                 default=Status.ACTIVE)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_edited_date = models.DateTimeField(auto_now=True)
    # owner_id
