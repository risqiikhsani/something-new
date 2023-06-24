from django.test import TestCase

# Create your tests here.

from .models import *
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
User = get_user_model()


class PostTestCase(APITestCase):
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

        self.post_list_url = reverse('post-list')

    def authenticate(self, is_staff=False):
        response = self.client.post(self.register_url, self.register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)
        # self.assertEqual(User.objects.get(id=1).username, self.register_data['username'])

        if is_staff:
            user = User.objects.get(id=1)
            user.is_staff = True
            user.save()

        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access_token']}")

    def test_post_create(self):
        self.authenticate()
        self.create_post_data = {
            "text":"hello"
        }
        response = self.client.post(self.post_list_url,self.create_post_data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.all().count(),1)
        self.assertEqual(Post.objects.get(id=1).text , self.create_post_data['text'])

    def test_post_list(self):
        self.authenticate()
        response = self.client.get(self.post_list_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        



    # def test_should_not_create_todo_with_no_auth(self):
    #     pass

    # def test_should_create_todo_with_auth(self):
    #     self.test_authenticate()

