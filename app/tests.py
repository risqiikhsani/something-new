from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()


class PostTestCase(APITestCase):
    def setUp(self):
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
        self.post = None

    def register_user(self):
        url = reverse('register')
        response = self.client.post(url, self.register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)
        self.user = User.objects.get(username=self.register_data['username'])

    def login_user(self):
        url = reverse('login')
        response = self.client.post(url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access_token']}")

    def create_post(self):
        self.post = Post.objects.create(text="test", user=self.user)

    def test_post_create(self):
        self.register_user()
        self.login_user()
        create_post_data = {
            "text": "hello"
        }
        url = reverse('post-list')
        response = self.client.post(url, create_post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(Post.objects.get(id=1).text, create_post_data['text'])
        self.assertEqual(Post.objects.get(id=1).user, self.user)

    def test_post_list(self):
        self.register_user()
        self.login_user()
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_detail(self):
        self.register_user()
        self.login_user()
        self.create_post()
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], self.post.text)

    def test_post_detail_update(self):
        self.register_user()
        self.login_user()
        self.create_post()
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        update_post_data = {
            "text": "hi",
        }
        response = self.client.put(url, update_post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], update_post_data['text'])
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, update_post_data['text'])

    def test_post_detail_delete(self):
        self.register_user()
        self.login_user()
        self.create_post()
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.all().count(), 0)
