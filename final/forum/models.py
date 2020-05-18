from django.contrib.auth.models import User
from django.db import models


class ForumUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f'User: {self.user.username}'

    def update_points(self):
        for post in self.post:
            for point in post.point:
                self.points += point


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
    value = models.CharField(max_length=1024, blank=False)
    user = models.ForeignKey(ForumUser, on_delete=models.CASCADE, related_name="post")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="post")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post: {self.user.user.username}: {self.value[:100]}'


class Points(models.Model):
    value = models.IntegerField(default=1)
    user = models.ForeignKey(ForumUser, on_delete=models.CASCADE, related_name="point")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="point")
