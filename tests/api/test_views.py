from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from urllib.parse import urlparse
from api.models import Submission


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


class FileUploadTests(APITestCase):

    def setUp(self):
        self.tearDown()
        self.test_user = UserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            full_name='Test User')
        self.test_user_token = Token.objects.create(user=self.test_user)

    def tearDown(self):
        try:
            u = UserModel.objects.get_by_natural_key('testuser')
            u.delete()

        except ObjectDoesNotExist:
            pass
        Submission.objects.all().delete()

    def _create_test_file(self, path):
        f = open(path, 'w')
        f.write('test123\n')
        f.close()
        f = open(path, 'rb')
        return {'datafile': f}

    def test_upload_file(self):
        url = reverse('submission-upload')
        data = self._create_test_file('/tmp/test_upload')
        client = self.client
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key)
        response = client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('created', response.data)

        self.assertTrue(urlparse(
            response.data['datafile']).path.startswith(settings.MEDIA_URL))
        self.assertEqual(
            response.data['owner'],
            UserModel.objects.get(username='testuser').username)
        self.assertIn('created', response.data)

        # assert unauthenticated user can not upload file
        client.logout()
        response = client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
