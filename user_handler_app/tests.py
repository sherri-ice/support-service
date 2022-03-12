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
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_id(self):
        user = User.objects.create_user(username='test', password='test',
                                        email='test@test.com')
        data = {
            'username': 'test',
            'password': 'test'
        }
        url = reverse('auth:token_obtain_pair')
        response = self.client.post(url, data, format='json')
        token = response.data['access']
        url = reverse('auth:users-me')

        # Correct request
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], user.id)

        # Bad request: wrong token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + "abc")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # TODO: logout

