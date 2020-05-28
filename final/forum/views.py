from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
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


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            ForumUser.objects.create(user=user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'forum/register.html', {'form': form})
