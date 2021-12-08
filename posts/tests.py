from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_posts(self):
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')
        User.objects.create_user(username='tom', password='password')

    def test_user_can_retrieve_post_with_id(self):
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')
        response = self.client.get('/posts/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_not_retrieve_post_with_invalid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_can_update_post_they_own(self):
        self.client.login(username='adam', password='pass')
        self.client.post('/posts/', {'title': 'a title'})
        response = self.client.put('/posts/1/', {'title': 'updated title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_can_not_update_posts_they_do_not_own(self):
        self.client.login(username='adam', password='pass')
        self.client.post('/posts/', {'title': 'a title'})
        self.client.logout()
        self.client.login(username='tom', password='password')
        response = self.client.put('/posts/1/', {'title': 'updated title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
