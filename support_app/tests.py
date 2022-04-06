from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from user_handler_app.models import User
from support_app.models import Ticket


# TODO: write token auth word
# from support_site.settings import SIMPLE_JWT

class TicketsAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test',
                                             email='test@test.com')
        self.another_user = User.objects.create_user(username='another_test',
                                                     password='test',
                                                     email='another_test@test.com')

        url = reverse('auth:token_obtain_pair')
        data = {
            'username': 'test',
            'password': 'test'
        }
        response = self.client.post(url, data, format='json')
        self.token = response.data['access']
        url = reverse('auth:token_obtain_pair')
        data = {
            'username': 'another_test',
            'password': 'test'
        }
        response = self.client.post(url, data, format='json')
        self.another_token = response.data['access']

        # Test ticket
        self.ticket = Ticket.objects.create(title="Test", body_text="test",
                                            owner=self.user)

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

    def test_get_all_tickets(self):
        url = reverse('tickets')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_ticket(self):
        url = reverse('ticket', args=[self.ticket.id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.ticket.id)

    def test_change_ticket_status(self):
        def test_user():
            url = reverse('ticket', args=[self.ticket.id])
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer  ' + self.another_token)
            data = {
                "status": "FR"
            }
            return self.client.patch(url, data=data, format='json')

        self.another_user.is_staff = False
        response = test_user()
        # Non-admin user can't change status
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Make admin
        self.another_user.is_admin = True
        self.another_user.is_staff = True
        self.another_user.save()
        response = test_user()

        # Admin can change status of the ticket
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # get ticket by id: permissions and auth
    # ? get tickets last status by id
    # change ticket status by id
