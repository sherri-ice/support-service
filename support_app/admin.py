from django.contrib import admin
from .models import Message, Ticket, User

admin.site.register(Message)
admin.site.register(Ticket)
admin.site.register(User)
