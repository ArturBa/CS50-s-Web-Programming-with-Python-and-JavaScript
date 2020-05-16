from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    value = models.CharField(max_length=1024)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post: {self.user_id.username}: {self.value[:100]}'


class Topic(models.Model):
    title = models.CharField(max_length=128)
    posts = models.ManyToManyField(Post, blank=False, related_name='topic')

    def __str__(self):
        return f"Topic: {self.title}"


class Theme(models.Model):
    title = models.CharField(max_length=128)
    topics = models.ManyToManyField(Topic, blank=False, related_name="theme")

    def __str__(self):
        return f'Theme: {self.title}'
