from django.urls import path

from . import views, utils

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
    path("update/sub", utils.update_sub, name="update_sub"),
    path("update/pizza", utils.update_pizza, name="update_pizza"),
    path("update/salad", utils.update_salad, name="update_salad"),
    path("update/pasta", utils.update_pasta, name="update_pasta"),
    path("update/dinner", utils.update_dinner, name="update_dinner"),
    path("checkout", views.checkout_view, name="checkout"),
    path("make_order", views.make_order, name="make_order"),
    path("user", views.user_view, name="user"),
    path("add/", utils.add, name="add"),
    path("order/update", utils.update_order, name="update_order")
]
