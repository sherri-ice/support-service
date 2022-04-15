from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
from django.utils import timezone


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


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(db_index=True, unique=True)
    date_joined = models.DateTimeField(default=timezone.now, auto_created=True)
    last_login = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()
