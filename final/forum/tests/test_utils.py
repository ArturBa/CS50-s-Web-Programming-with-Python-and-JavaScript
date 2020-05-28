from django.test import TestCase, Client
from django.urls import reverse

from ..utils import *


class NewPostUtilTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user('test_user', 'test@user.com', 'test123')
        cls.fuser = ForumUser.objects.create(user=cls.user)
        cls.theme = Theme.objects.create(title="test")
        cls.topic = Topic.objects.create(title="test topic", theme=cls.theme)

    def test_util_url_exists_at_desired_location(self):
        self.client.login(username='test_user', password='test123')
        response = self.client.post('/new-post/', data={'topic': self.topic.id, 'message': 'Test'})
        self.assertEqual(response.status_code, 200)

    def test_util_url_accessible_by_name(self):
        self.client.login(username='test_user', password='test123')
        response = self.client.post(reverse('new_post'), data={'topic': self.topic.id, 'message': 'Test'})
        self.assertEqual(response.status_code, 200)

    def test_util_no_login_forbidden(self):
        response = self.client.post(reverse('new_post'), data={'topic': self.topic.id, 'message': 'Test'})
        self.assertEqual(response.status_code, 302)


class AddPointUtilTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user('test_user', 'test@user.com', 'test123')
        cls.fuser = ForumUser.objects.create(user=cls.user)
        cls.theme = Theme.objects.create(title="test")
        cls.topic = Topic.objects.create(title="test topic", theme=cls.theme)
        cls.post = Post.objects.create(message="test topic", user=cls.fuser, topic=cls.topic)

    def test_util_url_exists_at_desired_location(self):
        self.client.login(username='test_user', password='test123')
        response = self.client.post('/add-point/', data={'post': self.post.id})
        self.assertEqual(response.status_code, 200)

    def test_util_url_accessible_by_name(self):
        self.client.login(username='test_user', password='test123')
        response = self.client.post(reverse('add_point'), data={'post': self.post.id})
        self.assertEqual(response.status_code, 200)

    def test_util_no_login_forbidden(self):
        response = self.client.post(reverse('add_point'), data={'post': self.post.id})
        self.assertEqual(response.status_code, 302)


class LoginUtilTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user('test_user', 'test@user.com', 'test123')

    def test_util_url_exists_at_desired_location(self):
        response = self.client.post('/login/', {'username': 'test_user', 'password': 'test123'})
        self.assertEqual(response.status_code, 200)

    def test_util_url_accessible_by_name(self):
        response = self.client.post(reverse('login'), {'username': 'test_user', 'password': 'test123'})
        self.assertEqual(response.status_code, 200)

    def test_util_url_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'test_user', 'password': 'nopass'})
        self.assertEqual(response.status_code, 401)

    def test_util_url_invalid_method(self):
        response = self.client.get(reverse('login'), {'username': 'test_user', 'password': 'nopass'})
        self.assertEqual(response.status_code, 400)
