from django.db import models
from django.utils.translation import gettext_lazy


class Message(models.Model):
    text = models.TextField()
    media_url = models.URLField(blank=True)
    send_date = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey('Ticket', related_name="messages",
                               on_delete=models.CASCADE)
    owner = models.ForeignKey('user_handler_app.User', related_name='messages',
                              on_delete=models.CASCADE)


class Ticket(models.Model):
    class Statuses(models.TextChoices):
        ACTIVE = 'AC', gettext_lazy('Active')
        FROZEN = 'FR', gettext_lazy('Frozen')
        CLOSED = 'CL', gettext_lazy('Closed')

    title = models.CharField(max_length=255)
    body_text = models.TextField()
    media_url = models.URLField(blank=True)
    status = models.CharField(max_length=2, choices=Statuses.choices,
                              default=Statuses.ACTIVE)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_edited_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('user_handler_app.User', related_name='tickets',
                              on_delete=models.CASCADE)
