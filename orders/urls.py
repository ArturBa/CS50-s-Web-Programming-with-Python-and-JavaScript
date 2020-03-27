from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("menu", views.menu_view, name="menu"),
    path("about_us", views.about_us_view, name="about_us"),
    path("login", views.login_view, name="login"),
    path("login_auth", views.login_authenticate, name="login_auth"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("orders", views.orders_view, name="orders"),
    path("cart", views.cart_view, name="cart"),
    path("update/sub", views.update_sub, name="update_sub"),
    path("update/pizza", views.update_pizza, name="update_pizza"),
    path("add/", views.add, name="add")
]
