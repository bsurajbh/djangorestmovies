from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

REGISTER_URL = reverse('register')
LOGIN_URL = reverse('login')


class UserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # create user
        self.username = 'manual'
        self.password = 'password@123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            first_name="fanme",
            last_name="lname",
            email="manual@test.com"
        )

    def test_login_url(self):
        response = self.client.get(LOGIN_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_register(self):
        payload = {
            "username": "user1",
            "password": "password@123",
            "first_name": "fanme",
            "last_name": "lname",
            "email": "test@test.com"
        }
        response = self.client.post(REGISTER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # duplicate user registration
        payload = {
            "username": "user1",
            "password": "password@123",
            "first_name": "fanme",
            "last_name": "lname",
            "email": "test@test.com"
        }
        response = self.client.post(REGISTER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        payload = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(LOGIN_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
