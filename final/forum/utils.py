from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import *
from .models import *


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            topic_id = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            fuser = ForumUser.objects.get(user=request.user)
            Post.objects.create(user=fuser, topic_id=topic_id, message=message)
            return HttpResponse('Post added', status=200)
        return HttpResponse('Form not valid', status=400)
    return HttpResponse('Not POST method', status=400)
