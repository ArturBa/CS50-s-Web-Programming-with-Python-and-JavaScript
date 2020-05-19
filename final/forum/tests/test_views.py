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
        number_of_topic = 13
        theme = Theme.objects.create(title="test")

        for topic_id in range(number_of_topic):
            Topic.objects.create(
                title=f'Topic test {topic_id}',
                theme=theme
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/topic/{Topic.objects.all()[0].id}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('topic', kwargs={'topic_id': Topic.objects.all()[0].id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('topic', kwargs={'topic_id': Topic.objects.all()[0].id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/topic.html')
