from django.shortcuts import render


def index(request):
    return render(request, 'forum/index.html')


def new_post(request):
    return render(request, 'forum/new-post.html')
