from django.test import TestCase

from .models import *
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.register_data = {
            "username": "testingusername",
            "email": "testing@gmail.com",
            "password": "password",
            "password2": "password",
        }
        self.login_data = {
            "username": "testingusername",
            "password": "password",
        }
        self.user = None

    def create_user(self):
        response = self.client.post(self.register_url, self.register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)
        self.user = User.objects.get(username=self.register_data['username'])

    def authenticate(self, is_staff=False):
        if not self.user:
            self.create_user()

        if is_staff:
            self.user.is_staff = True
            self.user.save()

        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access_token']}")

    def test_change_password(self):
        self.authenticate()
        self.change_password_url = reverse('change-password')
        self.change_password_data = {
            "old_password": "password",
            "password": "password123",
            "confirm_password": "password123",
        }
        response = self.client.put(self.change_password_url, self.change_password_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.login_data['password'] = "password123"
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
