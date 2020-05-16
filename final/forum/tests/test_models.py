from django.test import TestCase

from ..models import *


class PostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test')

    def setUp(self):
        self.p = Post.objects.create(value="Test", user_id=self.user)

    def test_creation(self):
        self.assertEqual("Test", self.p.value)
        self.assertTrue(isinstance(self.p, Post))


class TopicTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test')
        cls.post = Post.objects.create(value="test", user_id=cls.user)

    def setUp(self):
        self.t = Topic.objects.create(title="Test")
        self.t.posts.set([self.post])

    def test_creation(self):
        self.assertEqual("Test", self.t.title)
        self.assertTrue(isinstance(self.t, Topic))


class ThemeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test')
        cls.post = Post.objects.create(value="test", user_id=cls.user)
        cls.topic = Topic.objects.create(title="Test")
        cls.topic.posts.set([cls.post])

    def setUp(self):
        self.t = Theme.objects.create(title='Test')
        self.t.topics.set([self.topic])

    def test_creation(self):
        self.assertTrue(isinstance(self.t, Theme))
        self.assertEqual("Test", self.t.title)
