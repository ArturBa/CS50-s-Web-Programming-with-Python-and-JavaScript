from datetime import datetime

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


def add(request):
    if request.method != 'POST':
        return HttpResponse('', status=400)
    try:
        type = request.POST['type']
        if type == "pizza":
            add_pizza(request)
        elif type == "sub":
            add_sub(request)
        elif type == "salad":
            add_salad(request)
        elif type == "pasta":
            add_pasta(request)
        elif type == "dinner":
            add_dinner(request)
        else:
            return HttpResponse('', status=400)
        return HttpResponse('', status=200)
    except Exception as exception:
        print(exception)
        return HttpResponse('', status=400)


def is_large(request):
    if request.POST['large'] == 'False':
        return False
    else:
        return True


def add_pizza(request):
    id = request.POST['id']
    large = is_large(request)
    pizza_order = PizzaOrder.objects.create(pizza_id=Pizza.objects.get(id=id), large=large)
    pizza_order.save()
    status = OrderStatus.objects.get_or_create(name="In shopping cart")[0]
    cart = Order.objects.get_or_create(user_id=request.user, status=status)[0]
    cart.pizza_order.add(pizza_order)
    cart.save()


def add_sub(request):
    id = request.POST['id']
    large = is_large(request)
    sub_order = SubsOrder.objects.create(sub_id=Sub.objects.get(id=id), large=large)
    sub_order.save()
    status = OrderStatus.objects.get_or_create(name="In shopping cart")[0]
    cart = Order.objects.get_or_create(user_id=request.user, status=status)[0]
    cart.sub_order.add(sub_order)
    cart.save()


def add_salad(request):
    id = request.POST['id']
    salad_order = SaladOrder.objects.create(salad_id=Salad.objects.get(id=id))
    salad_order.save()
    print(salad_order)
    status = OrderStatus.objects.get_or_create(name="In shopping cart")[0]
    cart = Order.objects.get_or_create(user_id=request.user, status=status)[0]
    cart.salad_order.add(salad_order)
    cart.save()


def add_pasta(request):
    id = request.POST['id']
    pasta_order = PastaOrder.objects.create(pasta_id=Pasta.objects.get(id=id))
    pasta_order.save()
    status = OrderStatus.objects.get_or_create(name="In shopping cart")[0]
    cart = Order.objects.get_or_create(user_id=request.user, status=status)[0]
    cart.pasta_order.add(pasta_order)
    cart.save()


def add_dinner(request):
    id = request.POST['id']
    large = is_large(request)
    dinner_order = DinnerPlateOrder.objects.create(dinner_plate_id=DinnerPlate.objects.get(id=id), large=large)
    dinner_order.save()
    status = OrderStatus.objects.get_or_create(name="In shopping cart")[0]
    cart = Order.objects.get_or_create(user_id=request.user, status=status)[0]
    cart.dinner_plate_order.add(dinner_order)
    cart.save()


def update_sub(request):
    if request.method != 'POST':
        return HttpResponse('Wrong method', status=400)
    try:
        id = request.POST['id']
        quantity = int(request.POST.get('quantity'))
        sub = SubsOrder.objects.get(id=id)
        if quantity == 0:
            sub.delete()
            return HttpResponse('Sub Order deleted', status=200)

        cheese = True if request.POST.get('cheese', False) else False
        big = True if request.POST.get('big', False) else False
        adds = request.POST.getlist('adds')
        print(f'Id: {id} q: {quantity} cheese: {cheese} big: {big} add: {adds}')

        sub.quantity = quantity
        sub.extra_cheese = cheese
        sub.large = big
        sub.adds.clear()
        for add_id in adds:
            sub.adds.add(SubAdd.objects.get(id=add_id))
        sub.save()
        return HttpResponse('Sub updated', status=200)
    except Exception as exception:
        print(exception)
        return HttpResponse(f'Exception {exception}', status=400)


def update_pizza(request):
    if request.method != 'POST':
        return HttpResponse('Wrong method', status=400)
    try:
        id = request.POST['id']
        quantity = int(request.POST.get('quantity'))
        order = PizzaOrder.objects.get(id=id)
        if quantity == 0:
            order.delete()
            return HttpResponse('Pizza order deleted', status=200)

        big = True if request.POST.get('big', False) else False
        toppings = request.POST.getlist('toppings')
        print(f'Pizza id: {id} q: {quantity} big: {big} toppings: {toppings}')

        order.quantity = quantity
        order.large = big
        order.toppings.clear()
        for top_id in toppings:
            order.toppings.add(Topping.objects.get(id=top_id))
        order.save()
        return HttpResponse('Pizza order updated', status=200)
    except Exception as exception:
        print(exception)
        return HttpResponse(f'Exception {exception}', status=400)


def update_salad(request):
    if request.method != 'POST':
        return HttpResponse('Wrong method', status=400)
    try:
        id = request.POST['id']
        quantity = int(request.POST.get('quantity'))
        order = SaladOrder.objects.get(id=id)
        if quantity == 0:
            order.delete()
            return HttpResponse('Salad order deleted', status=200)

        order.quantity = quantity
        order.save()
        print(f'Salad id: {id} q: {quantity}')
        return HttpResponse('Salad order updated', status=200)
    except Exception as exception:
        print(exception)
        return HttpResponse(f'Exception {exception}', status=400)


def update_pasta(request):
    if request.method != 'POST':
        return HttpResponse('Wrong method', status=400)
    try:
        id = request.POST['id']
        quantity = int(request.POST.get('quantity'))
        order = PastaOrder.objects.get(id=id)
        if quantity == 0:
            order.delete()
            return HttpResponse('Pasta order deleted', status=200)

        order.quantity = quantity
        order.save()
        print(f'Pasta id: {id} q: {quantity}')
        return HttpResponse('Pasta order updated', status=200)
    except Exception as exception:
        print(type(exception))
        return HttpResponse(f'Exception {exception}', status=400)


def update_dinner(request):
    if request.method != 'POST':
        return HttpResponse('Wrong method', status=400)
    try:
        id = request.POST['id']
        quantity = int(request.POST.get('quantity'))
        order = DinnerPlateOrder.objects.get(id=id)
        if quantity == 0:
            order.delete()
            return HttpResponse('Dinner plate order deleted', status=200)

        big = True if request.POST.get('big', False) else False

        order.quantity = quantity
        order.large = big
        order.save()
        print(f'Dinner id: {id} q: {quantity} big: {big}')
        return HttpResponse('Dinner plate order updated', status=200)
    except Exception as exception:
        print(type(exception))
        return HttpResponse(f'Exception {exception}', status=400)


def update_order(request):
    if request.method != 'POST':
        return HttpResponse('Wrong method', status=400)
    try:
        id = request.POST['id']
        order = Order.objects.get(id=id)
        new_status = request.POST['status']
        order.status = OrderStatus.objects.get_or_create(name=new_status)[0]
        order.save()
    except Exception as exception:
        print(exception)
        print(type(exception))
        return HttpResponse(f'Exception {exception}', status=400)
