from django.test import TestCase

from ..models import *


class PostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        user = User.objects.create(username='test')
        cls.p = Post.objects.create(value="Test", user_id=user)
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_creation(self):
        print("Method: test_creation.")
        self.assertEqual("Test", self.p.value)
        self.assertTrue(isinstance(self.p, Post))
