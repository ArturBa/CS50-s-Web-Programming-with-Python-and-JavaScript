from django.urls import path

from . import utils
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user/", views.user, name="user"),
    path("user/<str:username>/", views.user, name="user"),
    path("topic/", views.topic, name="topic"),
    path("topic/<int:topic_id>/", views.topic, name="topic"),
    path('new-post/', utils.new_post, name='new_post'),
    path('add-point/', utils.add_point, name='add_point'),
    path('login/', utils.login_auth, name='login'),
    path('logout/', utils.logout_auth, name='logout'),
    path('register/', views.register_view, name='register')
]
