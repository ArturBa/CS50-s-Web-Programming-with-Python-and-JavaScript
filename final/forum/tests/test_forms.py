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
    def test_UserForm_missing_value(self):
        form = PostForm(data={'topic': '', 'message': "mp"})
        self.assertFalse(form.is_valid())

    def test_UserForm_wrong_value(self):
        form = PostForm(data={'topic': 'test', 'message': "mp"})
        self.assertFalse(form.is_valid())


class PointFormTest(TestCase):
    @classmethod
    def setUp(cls):
        pass

    def test_PointForm_valid(self):
        form = PointForm(data={'post': 1})
        self.assertTrue(form.is_valid())

    def test_PointForm_missing_data(self):
        form = PointForm(data={'post': ''})
        self.assertFalse(form.is_valid())

    def test_PointForm_wrong_value(self):
        form = PointForm(data={'post': 'test'})
        self.assertFalse(form.is_valid())


class TopicFormTest(TestCase):
    @classmethod
    def setUp(cls):
        pass

    def test_TopicForm_valid(self):
        form = TopicForm(data={'theme': 1, 'topic': 'test', 'message': 'text'})
        self.assertTrue(form.is_valid())

    def test_TopicForm_missing_data(self):
        form = TopicForm(data={'theme': ''})
        self.assertFalse(form.is_valid())

    def test_TopicForm_wrong_value(self):
        form = TopicForm(data={'theme': 'test'})
        self.assertFalse(form.is_valid())
