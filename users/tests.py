from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFollowTests(APITestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password123')
        self.user3 = User.objects.create_user(username='user3', email='user3@example.com', password='password123')

        response = self.client.post('/api/v1/authentication/token/', {
            'username': 'user1',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_follow_user(self):
        url = reverse('follow_user', args=['user2'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_self(self):
        url = reverse('follow_user', args=['user1'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "You can't follow yourself.")

    def test_already_following_user(self):
        response = self.client.post(reverse('follow_user', args=['user2']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(reverse('follow_user', args=['user2']))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "You are already following user2.")

    def test_unfollow_user(self):
        self.user1.following.add(self.user2)
        url = reverse('unfollow_user', args=['user2'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.user2, self.user1.following.all())
        self.assertEqual(response.data['message'], 'You have unfollowed user2')

    def test_unfollow_self(self):
        url = reverse('unfollow_user', args=['user1'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'You cannot unfollow yourself.')

    def test_not_following_user(self):
        url = reverse('unfollow_user', args=['user2'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'You are not following this user.')

    def test_follow_nonexistent_user(self):
        url = reverse('follow_user', args=['nonexistent_user'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No User matches the given query.')

    def test_follow_after_unfollow(self):
        self.user1.following.add(self.user2)
        self.user1.following.remove(self.user2)
        url = reverse('follow_user', args=['user2'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user2, self.user1.following.all())

    def test_follow_user_without_auth(self):
        self.client.credentials()
        url = reverse('follow_user', args=['user2'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_new_user_following_empty(self):
        self.assertEqual(self.user1.following.count(), 0)

    def test_unfollow_all_users(self):
        self.user1.following.add(self.user2)
        self.user1.following.add(self.user3)
        self.assertEqual(self.user1.following.count(), 2)

        self.client.post(reverse('unfollow_user', args=['user2']))
        self.client.post(reverse('unfollow_user', args=['user3']))

        self.assertEqual(self.user1.following.count(), 0)
