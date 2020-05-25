from django.test import TestCase
from django.urls import reverse

from ..models import *


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 topics for tests
        number_of_topic = 13
        theme = Theme.objects.create(title="test")

        for topic_id in range(number_of_topic):
            Topic.objects.create(
                title=f'Topic test {topic_id}',
                theme=theme
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/index.html')

    def test_lists_all_themes(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['themes']) == 1)
        self.assertTrue(len(response.context['themes'][0].topic.all()) == 13)


class TopicViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_posts = 13
        theme = Theme.objects.create(title="test")
        user = User.objects.create(username='test_user')
        fuser = ForumUser.objects.create(user=user)
        cls.topic = Topic.objects.create(title='title', theme=theme)

        for post in range(number_of_posts):
            Post.objects.create(
                message=f'Topic test {post}',
                topic=cls.topic,
                user=fuser
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/topic/{self.topic.id}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('topic', kwargs={'topic_id': self.topic.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('topic', kwargs={'topic_id': self.topic.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic.html')
        self.assertEqual(response.context['topic'].id, self.topic.id)

    def test_view_show_10_posts(self):
        response = self.client.get(reverse('topic', kwargs={'topic_id': self.topic.id}))
        self.assertEqual(len(response.context['posts']), 10)

    def test_view_show_3_posts_page_2(self):
        response = self.client.get(reverse('topic', kwargs={'topic_id': self.topic.id}) + '?page=1')
        self.assertEqual(len(response.context['posts']), 3)

    def test_view_default_on_100_page(self):
        response = self.client.get(reverse('topic', kwargs={'topic_id': self.topic.id}) + '?page=10')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.context['posts']), 10)


class UserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test')
        cls.fuser = ForumUser.objects.create(user=cls.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/user/{self.user.username}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('user', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('user', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/user.html')
        self.assertEqual(response.context['forum_user'].id, self.fuser.id)
