from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    context = {
        'themes': Theme.objects.all()
    }
    return render(request, 'forum/index.html', context)


def user(request, username):
    try:
        user_w_username = User.objects.get(username=username)
        context = {
            'forum_user': ForumUser.objects.get(user=user_w_username),
            'forum_activity': ForumUser.objects.get(user=user_w_username).post.order_by('-date').all()[:10]
        }
        return render(request, 'forum/user.html', context)
    except Exception as e:
        print(e)
        return render(request, 'forum/no-user.html')


def topic(request, topic_id):
    try:
        page = int(request.GET['page'])
    except Exception:
        page = 0
    try:
        if len(Post.objects.filter(topic_id=topic_id).all()[page * 10: page * 10 + 10]) == 0:
            return HttpResponseRedirect(reverse(f'topic', kwargs={'topic_id': topic_id}))
        context = {
            'topic': Topic.objects.get(id=topic_id),
            'posts': Post.objects.filter(topic_id=topic_id).all()[page * 10: page * 10 + 10],
            'max_page': int(Post.objects.filter(topic_id=topic_id).count() / 10)
        }
        return render(request, 'forum/topic.html', context)
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse('index'))
