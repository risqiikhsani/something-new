from django.test import TestCase

# Create your tests here.

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
            "username":"testingusername",
            "email":"testing@gmail.com",
            "password":"password",
            "password2":"password",
        }
        self.login_data = {
            "username":"testingusername",
            "password":"password",
        }

    def authenticate(self, is_staff=False):
        response = self.client.post(self.register_url, self.register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)

        if is_staff:
            user = User.objects.get(id=1)
            user.is_staff = True
            user.save()

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

        self.login_data = {
            "username": "testingusername",
            "password": "password123",
        }

        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        



    # def test_should_not_create_todo_with_no_auth(self):
    #     pass

    # def test_should_create_todo_with_auth(self):
    #     self.test_authenticate()

