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
    path("update/salad", views.update_salad, name="update_salad"),
    path("update/pasta", views.update_pasta, name="update_pasta"),
    path("update/dinner", views.update_dinner, name="update_dinner"),
    path("checkout", views.checkout_view, name="checkout"),
    path("make_order", views.make_order, name="make_order"),
    path("add/", views.add, name="add")
]
