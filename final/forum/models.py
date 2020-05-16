from django.contrib.auth.models import User
from django.db import models


class Theme(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return f'Theme: {self.title}'


class Topic(models.Model):
    title = models.CharField(max_length=128)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="topic")

    def __str__(self):
        return f"Topic: {self.title}"


class Post(models.Model):
    value = models.CharField(max_length=1024, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="post")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post: {self.user.username}: {self.value[:100]}'
