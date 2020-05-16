from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    value = models.CharField(max_length=1024)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    date = models.DateTimeField(auto_now_add=True)


class Topic(models.Model):
    title = models.CharField(max_length=128)
    posts = models.ManyToManyField(Post, blank=False, related_name='topic')


class Theme(models.Model):
    title = models.CharField(max_length=128)
    topics = models.ManyToManyField(Topic, blank=False, related_name="theme")
