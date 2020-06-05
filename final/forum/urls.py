from django.urls import path

from . import utils
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user/", views.user, name="user"),
    path("user/<str:username>/", views.user, name="user"),
    path("topic/", views.topic, name="topic"),
    path("topic/<int:topic_id>/", views.topic, name="topic"),
    path('new-post/', utils.new_post, name='new-post'),
    path('add-point/', utils.add_point, name='add-point'),
    path('login/', utils.login_auth, name='login'),
    path('logout/', utils.logout_auth, name='logout'),
    path('register/', views.register_view, name='register'),
    path('new-topic/<int:theme_id>', views.new_topic_view, name='new-topic'),
    path('add-topic/', utils.add_topic, name='add-topic')
]
