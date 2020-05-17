from django.shortcuts import render

from .models import *


def index(request):
    context = {
        'themes': Theme.objects.all()
    }
    return render(request, 'forum/index.html', context)


def new_post(request):
    return render(request, 'forum/new-post.html')
