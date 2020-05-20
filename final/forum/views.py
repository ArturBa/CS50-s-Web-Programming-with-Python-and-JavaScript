from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *
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
            'forum_activity': ForumUser.objects.get(user=user_w_username).post.all()
        }
        return render(request, 'forum/user.html', context)
    except Exception as e:
        print(e)
        return render(request, 'forum/no-user.html')


def topic(request, topic_id):
    try:
        context = {
            'topic': Topic.objects.get(id=topic_id),
            'form': PostForm()
        }
        return render(request, 'forum/topic.html', context)
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse('index'))


def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user']
            topic_id = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            Post.objects.create(user_id=user_id, topic_id=topic_id, message=message)
        return HttpResponseRedirect(reverse(f"topic/{request.POST['topic']}"))
    return HttpResponseRedirect(reverse("index"))
