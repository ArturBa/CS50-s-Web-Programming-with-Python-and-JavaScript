from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(ForumUser)
admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Theme)
admin.site.register(Point)
