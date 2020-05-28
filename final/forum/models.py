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

    def recent_topics(self):
        topics_by_post_date = self.topic.order_by('-post__date').all()
        unique_topic_id = []
        i = 0
        for topic in topics_by_post_date:
            if topic.id not in unique_topic_id:
                i += 1
                unique_topic_id.append(topic.id)
                if i == 10:
                    break

        topics = []
        for unique_topic in unique_topic_id:
            topics.append(Topic.objects.get(id=unique_topic))
        return topics


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
