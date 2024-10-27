from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class PostTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password123')
        
        response = self.client.post('/api/v1/authentication/token/', {'username': 'user1', 'password': 'password123'})
        token = self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        self.post_data = {
            'title': 'Test Post',
            'content': 'This is a test post.',
        }
        response = self.client.post('/api/v1/authentication/token/', {'username': 'user1', 'password': 'password123'})
        token = self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_post(self):
        url = reverse('post_list_create')
        response = self.client.post(url, self.post_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().content, 'This is a test post.')

    def test_create_post_unauthenticated(self):
        self.client.logout()
        url = reverse('post_list_create')
        response = self.client.post(url, self.post_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_post(self):
        post = Post.objects.create(**self.post_data, author=self.user1)
        url = reverse('post_detail', args=[post.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['post']['content'], post.content)
        self.assertEqual(response.data['post']['title'], post.title)


    def test_update_post(self):
        post = Post.objects.create(**self.post_data, author=self.user1)
        url = reverse('post_detail', args=[post.pk])
        updated_data = {
            'title': 'Updated Post',
            'content': 'This post has been updated.',
        }
        response = self.client.put(url, updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Post')

    def test_delete_post(self):
        post = Post.objects.create(**self.post_data, author=self.user1)
        url = reverse('post_detail', args=[post.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_like_post(self):
        post = Post.objects.create(**self.post_data, author=self.user2)
        url = reverse('like_post', args=[post.pk])
        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user1, post.likes.all())
