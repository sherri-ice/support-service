from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

from .models import User
from rest_framework_simplejwt.serializers import TokenObtainSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'email': {'required': True}
        }
