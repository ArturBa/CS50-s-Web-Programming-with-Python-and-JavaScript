from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import *
from .models import *


@login_required
def new_post(request):
    if request.method != 'POST':
        return HttpResponse('Not POST method', status=400)
    form = PostForm(request.POST)
    if not form.is_valid():
        return HttpResponse('Form not valid', status=400)
    topic_id = form.cleaned_data['topic']
    message = form.cleaned_data['message']
    fuser = ForumUser.objects.get(user=request.user)
    Post.objects.create(user=fuser, topic_id=topic_id, message=message)
    return HttpResponse('Post added', status=200)


@login_required
def add_point(request):
    if request.method != 'POST':
        return HttpResponse('Not POST method', status=400)
    form = PointForm(request.POST)
    if not form.is_valid():
        return HttpResponse('Form not valid', status=400)
    post_id = form.cleaned_data['post']
    fuser = ForumUser.objects.get(user=request.user)
    Points.objects.get_or_create(user=fuser, post_id=post_id)
    return HttpResponse('Point added', status=200)
