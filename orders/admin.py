from django.contrib import admin

from .models import *

admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(PizzaOrder)
admin.site.register(PizzaType)
admin.site.register(Sub)
admin.site.register(SubAdd)
admin.site.register(SubsOrder)
admin.site.register(Salad)
admin.site.register(SaladOrder)
admin.site.register(Pasta)
admin.site.register(PastaOrder)
admin.site.register(DinnerPlate)
admin.site.register(DinnerPlateOrder)
admin.site.register(OrderStatus)
admin.site.register(Order)
