from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
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
            return render(request, "orders/orders.html")
        else:
            return render(request, "orders/login.html",
                          {"message": "Look's like you dont have permissions here. Try relogin."})
    return render(request, "orders/login.html", {"message": "Login firstly"})


def cart_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reversed('index'))
    status = OrderStatus.objects.get_or_create(name="cart")[0]
    cart = Order.objects.get_or_create(user_id=request.user, status=status)[0]
    print(cart.pizza_order.all())
    return render(request, "orders/cart.html", {'cart': cart})


def add(request):
    if request.method != 'POST':
        return HttpResponse('', status=400)
    try:
        type = request.POST['type']
        if type == "pizza":
            add_pizza(request)
        # elif type == "sub":
        #     add_sub(request)
        print(f'{type}: {id}')
        return HttpResponse('', status=200)
    except Exception as exception:
        print(exception)
        return HttpResponse('', status=400)


def add_pizza(request):
    id = request.POST['id']
    if request.POST['large'] == 'False':
        large = False
    else:
        large = True
    pizza_order = PizzaOrder.objects.create(pizza_id=Pizza.objects.get(id=id), large=large)
    pizza_order.save()
    status = OrderStatus.objects.get_or_create(name="cart")[0]
    cart = Order.objects.get_or_create(user_id=request.user, status=status)[0]
    cart.pizza_order.add(pizza_order)
    cart.save()


def add_sub(request):
    id = request.POST['id']
    print(f'Sub: {id}')
