from django.shortcuts import render

from .models import *


def index(request):
    context = {
        'themes': Theme.objects.all()
    }
    print(Theme.objects.all()[0].topic.all()[0].post.last())
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


def new_post(request):
    return render(request, 'forum/new-post.html')
