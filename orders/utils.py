from django.http import HttpResponse

from .models import *


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
