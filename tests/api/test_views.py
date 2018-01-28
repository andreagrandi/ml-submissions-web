from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


UserModel = get_user_model()


class AccountsTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = UserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            full_name='Test User')

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'username': 'foobar',
            'full_name': 'Foo Bar',
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }

        url = reverse('account-create')
        response = self.client.post(url, data, format='json')

        self.assertEqual(UserModel.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['full_name'], data['full_name'])
        self.assertFalse('password' in response.data)

    def test_api_login(self):
        data = {
            'username': 'test@example.com',
            'password': 'testpassword'
        }

        url = reverse('api-login')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()['token'],
            Token.objects.all()[0].key
        )
