from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()


class Message(models.Model):
    text = models.TextField()
    media_url = models.URLField(blank=True)
    send_date = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey('Ticket', related_name="messages",
                               on_delete=models.CASCADE)
    owner = models.ForeignKey('User', related_name='messages',
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
    owner = models.ForeignKey('User', related_name='tickets',
                              on_delete=models.CASCADE)
