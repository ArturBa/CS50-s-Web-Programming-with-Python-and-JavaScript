from django.contrib.auth.models import User
from django.db import models


class ForumUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'User: {self.user.username}'

    def get_points(self):
        points = 0
        for post in self.post.all():
            points += post.get_points()
        return points


class Theme(models.Model):
    title = models.CharField(max_length=128)
    icon = models.CharField(max_length=512)

    def __str__(self):
        return f'Theme: {self.title}'


class Topic(models.Model):
    title = models.CharField(max_length=128)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="topic")

    def __str__(self):
        return f"Topic: {self.title}"


class Post(models.Model):
    message = models.CharField(max_length=1024, blank=False)
    user = models.ForeignKey(ForumUser, on_delete=models.CASCADE, related_name="post")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="post")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post: {self.user.user.username}: {self.message[:100]}'

    def get_points(self):
        points = 0
        for point in self.point.all():
            points += point.value
        return points


class Point(models.Model):
    value = models.IntegerField(default=1)
    user = models.ForeignKey(ForumUser, on_delete=models.CASCADE, related_name="point")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="point")
