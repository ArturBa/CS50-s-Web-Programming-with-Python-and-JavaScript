from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


# Create your views here.
def index(request):
    return render(request, "orders/index.html")


def login_view(request):
    return render(request, "orders/login.html", {"message": None})


def menu_view(request):
    return render(request, 'orders/menu.html')


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
    print('hi')
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
