from django.contrib.auth.models import User
from django.db import models


class Pizza(models.Model):
    """
    Pizza model
    """
    name = models.CharField(max_length=64)
    toppings_count = models.IntegerField()
    large_price = models.FloatField()
    small_price = models.FloatField()


class Topping(models.Model):
    """
    Topping model
    """
    name = models.CharField(max_length=64)


class PizzaOrder(models.Model):
    """
    Pizza order model. Contains size, toppings and quantity of pizza
    """
    pizza_id = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    large = models.BooleanField(default=True)
    quantity = models.IntegerField(default=1)
    toppings = models.ManyToManyField(Topping)


ORDER_STATUS_CHOICES = (
    ('wait', 'Waiting'),
    ('cook', 'Cooking'),
    ('delv', 'Delivering'),
    ('comp', 'Completed')
)


class Order(models.Model):
    """
    Order model
    """
    WAITING = 'FR'
    COOKING = 'SO'
    DELIVERING = 'JR'
    COMPLETED = 'SR'
    ORDER_STATUS_CHOICES = (
        (WAITING, 'Waiting'),
        (COOKING, 'Cooking'),
        (DELIVERING, 'Delivering'),
        (COMPLETED, 'Completed')
    )
    status = models.CharField(max_length=4, choices=ORDER_STATUS_CHOICES)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    pizza_order = models.ForeignKey(PizzaOrder, on_delete=models.CASCADE)
