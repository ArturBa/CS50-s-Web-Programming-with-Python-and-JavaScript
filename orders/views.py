from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "orders/index.html")


def login_view(request):
    return render(request, "orders/login.html", {"message": None})


def menu_view(request):
    context = {'pizza': PizzaType.objects.all(),
               'subs': Sub.objects.all(),
               'salads': Salad.objects.all(),
               'pastas': Pasta.objects.all(),
               'dinner_plates': DinnerPlate.objects.all()}
    return render(request, 'orders/menu.html', context)


def about_us_view(request):
    return render(request, 'orders/about_us.html')


def login_authenticate(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/login.html", {"message": "Invalid credentials."})


def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out."})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'orders/register.html', {'form': form})


def orders_view(request):
    if request.user.is_authenticated:
        groups = []
        for group in request.user.groups.all():
            groups.append(group.name)
        if 'cook' in groups:
            collecting_status = OrderStatus.objects.get_or_create(name="Collecting goods")[0]
            cooking_status = OrderStatus.objects.get_or_create(name="Cooking")[0]
            delivering_status = OrderStatus.objects.get_or_create(name="Delivering")[0]
            completed_status = OrderStatus.objects.get_or_create(name="Completed")[0]
            collecting_orders = Order.objects.filter(status=collecting_status).order_by('creation_date')
            delivering_orders = Order.objects.filter(status=delivering_status).order_by('creation_date')
            cooking_orders = Order.objects.filter(status=cooking_status).order_by('creation_date')
            completed_orders = Order.objects.filter(status=completed_status).order_by('creation_date')
            return render(request, "orders/orders.html",
                          {'collecting': collecting_orders, 'cooking': cooking_orders, 'delivering': delivering_orders,
                           'completed': completed_orders})
        else:
            return render(request, "orders/login.html",
                          {"message": "Look's like you dont have permissions here. Try relogin."})
    return render(request, "orders/login.html", {"message": "Login firstly"})


def cart_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    status = OrderStatus.objects.get_or_create(name="In shopping cart")[0]
    cart = Order.objects.get_or_create(user_id=request.user, status=status)[0]
    toppings = Topping.objects.all()
    sub_adds = SubAdd.objects.all()
    return render(request, "orders/cart.html", {'cart': cart, 'toppings': toppings, 'sub_adds': sub_adds})


def checkout_view(request):
    status = OrderStatus.objects.get_or_create(name="In shopping cart")[0]
    cart = Order.objects.get_or_create(user_id=request.user, status=status)[0]
    return render(request, "orders/checkout.html", {'cart': cart})


def make_order(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("index"))
    status = OrderStatus.objects.get_or_create(name="In shopping cart")[0]
    order = Order.objects.get_or_create(user_id=request.user, status=status)[0]
    status = OrderStatus.objects.get_or_create(name="Collecting goods")[0]
    order.status = status
    order.address = request.POST['address']
    order.add_info = request.POST['add_info']
    order.creation_date = datetime.now()
    order.save()
    return HttpResponseRedirect(reverse("index"))


def user_view(request):
    status = OrderStatus.objects.get_or_create(name="In shopping cart")[0]
    orders = Order.objects.filter(user_id=request.user.id).exclude(status=status).order_by('-creation_date')
    return render(request, "orders/user.html", {'orders': orders})
