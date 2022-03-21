from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from user_handler_app.models import User
from support_app.models import Ticket


class TicketsAPITests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='test', password='test',
                                 email='test@test.com')
        url = reverse('auth:token_obtain_pair')
        data = {
            'username': 'test',
            'password': 'test'
        }
        response = self.client.post(url, data, format='json')
        self.token = response.data['access']

    def test_create_ticket(self):
        url = reverse('create_ticket')
        data = {
            'title': 'test',
            'body_text': 'test',
            'status': 'AC'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tickets(self):
        Ticket.objects.create(title="Test", body_text="test");
        url = reverse('tickets')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.token)
        response = self.client.get(url, format='json')
        self.assertEqual(response)


    # get ticket by id: permissions and auth
    # ? get tickets last status by id
    # change ticket status by id
