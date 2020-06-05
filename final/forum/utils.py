from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

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
    Point.objects.get_or_create(user=fuser, post_id=post_id)
    return HttpResponse('Point added', status=200)


def login_auth(request):
    if request.method != 'POST':
        return HttpResponse('Not POST method', status=400)
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("User logged", status=200)
    else:
        return HttpResponse('Invalid credentials', status=401)


def logout_auth(request):
    logout(request)
    return HttpResponse("User logout", status=200)


@login_required
def add_topic(request):
    if request.method != 'POST':
        return HttpResponse('Not POST method', status=400)
    form = TopicForm(request.POST)
    if not form.is_valid():
        print('form not valid')
        return HttpResponse('Form not valid', status=400)
    theme_id = form.cleaned_data['theme']
    topic = form.cleaned_data['topic']
    message = form.cleaned_data['message']
    fuser = ForumUser.objects.get(user=request.user)
    topic_obj = Topic.objects.create(theme_id=theme_id, title=topic)
    Post.objects.create(topic=topic_obj, user=fuser, message=message)
    return JsonResponse(status=200, data={'msg': 'Post added', 'topic_id': topic_obj.id})
