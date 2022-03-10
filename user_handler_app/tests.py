import datetime

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import User


class UserTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('auth:register')
        data = {
            'username': 'test',
            'password': 'test',
            'email': 'test@test.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test')

    def test_login(self):
        """
        Ensure we can login as registered user.
        """
        User.objects.create_user(username='test', password='test',
                                 email='test@test.com')
        url = reverse('auth:token_obtain_pair')
        data = {
            'username': 'test',
            'password': 'test'
        }
        login_time, response = datetime.datetime.now(), self.client.post(url,
                                                                         data,
                                                                         format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            User.objects.filter(username=data['username']).get().last_login,
            login_time)
