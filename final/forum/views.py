from django.shortcuts import render

from .models import *


def index(request):
    context = {
        'themes': Theme.objects.all()
    }
    print(Theme.objects.all()[0].topic.all()[0].post.last())
    return render(request, 'forum/index.html', context)


def new_post(request):
    return render(request, 'forum/new-post.html')
