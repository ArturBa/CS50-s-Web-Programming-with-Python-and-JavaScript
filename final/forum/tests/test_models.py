from django.test import TestCase

from ..models import *


class PostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.theme = Theme.objects.create(title='test')
        cls.topic = Topic.objects.create(title="test", theme=cls.theme)
        cls.user = User.objects.create(username='test')
        cls.fuser = ForumUser.objects.create(user=cls.user)

    def setUp(self):
        self.p = Post.objects.create(message="Test", user=self.fuser, topic=self.topic)

    def test_creation(self):
        self.assertEqual("Test", self.p.message)
        self.assertTrue(isinstance(self.p, Post))


class TopicTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.theme = Theme.objects.create(title='test')

    def setUp(self):
        self.t = Topic.objects.create(title="Test", theme=self.theme)

    def test_creation(self):
        self.assertEqual("Test", self.t.title)
        self.assertTrue(isinstance(self.t, Topic))


class ThemeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        self.t = Theme.objects.create(title='Test')

    def test_creation(self):
        self.assertTrue(isinstance(self.t, Theme))
        self.assertEqual("Test", self.t.title)
