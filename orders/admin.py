from django.contrib import admin

from .models import *

admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(PizzaOrder)
admin.site.register(Order)
