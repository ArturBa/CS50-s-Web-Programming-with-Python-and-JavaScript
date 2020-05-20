from django.test import TestCase, Client
from django.urls import reverse

from ..utils import *


class NewPostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_user('test_user', 'test@user.com', 'test123')
        cls.fuser = ForumUser.objects.create(user=cls.user)
        cls.theme = Theme.objects.create(title="test")
        cls.topic = Topic.objects.create(title="test topic", theme=cls.theme)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='test_user', password='test123')
        response = self.client.post('/new-post/', data={'topic': self.topic.id, 'message': 'Test'})
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='test_user', password='test123')
        response = self.client.post(reverse('new_post'), data={'topic': self.topic.id, 'message': 'Test'})
        print(response)
        self.assertEqual(response.status_code, 200)
