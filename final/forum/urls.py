from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user/", views.user, name="user"),
    path("user/<str:username>/", views.user, name="user"),
    path("topic/", views.topic, name="topic"),
    path("topic/<int:topic_id>/", views.topic, name="topic"),
    path('new-post/', views.new_post, name='new_post')
]
