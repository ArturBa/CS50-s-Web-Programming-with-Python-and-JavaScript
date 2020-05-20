from django.test import TestCase

from ..forms import *


class PostFormTest(TestCase):
    @classmethod
    def setUp(cls):
        pass

    # Valid Form Data
    def test_PostForm_valid(self):
        form = PostForm(data={'topic': 12, 'message': "test_message"})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_UserForm_invalid(self):
        form = PostForm(data={'topic': '', 'message': "mp"})
        self.assertFalse(form.is_valid())
