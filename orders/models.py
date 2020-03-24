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

    def __str__(self):
        return f'Pizza: {self.name} with toppings: {self.toppings_count}'


class Topping(models.Model):
    """
    Topping model
    """
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'Topping: {self.name}'


class PizzaOrder(models.Model):
    """
    Pizza order model. Contains size, toppings and quantity of pizza
    """
    pizza_id = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    large = models.BooleanField(default=True)
    quantity = models.IntegerField(default=1)
    toppings = models.ManyToManyField(Topping, blank=True)


class SubAdd(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f'Sub add: {self.name}'


class Sub(models.Model):
    name = models.CharField(max_length=64)
    extra_cheese_price = models.FloatField(default=0.5)
    price_large = models.FloatField()
    price_small = models.FloatField()
    add_available = models.BooleanField()

    def __str__(self):
        return f'Sub: {self.name}'


class SubsOrder(models.Model):
    sub_id = models.ForeignKey(Sub, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    large = models.BooleanField(default=True)
    extra_cheese = models.BooleanField(default=False)
    adds = models.ManyToManyField(SubAdd, blank=True)


class Salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f'Salad: {self.name}'


class SaladOrder(models.Model):
    salad_id = models.ForeignKey(Salad, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f'Pasta: {self.name}'


class PastaOrder(models.Model):
    pasta_id = models.ForeignKey(Pasta, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class DinnerPlate(models.Model):
    name = models.CharField(max_length=64)
    price_large = models.FloatField()
    price_small = models.FloatField()

    def __str__(self):
        return f'Dinner Plate: {self.name}'


class DinnerPlateOrder(models.Model):
    dinner_plate_id = models.ForeignKey(DinnerPlate, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    large = models.BooleanField(default=True)


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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    creation_date = models.DateField(auto_now_add=True)
    pizza_order = models.ManyToManyField(PizzaOrder, blank=True)
    sub_order = models.ManyToManyField(SubsOrder, blank=True)
    salad_order = models.ManyToManyField(SaladOrder, blank=True)
    pasta_order = models.ManyToManyField(PastaOrder, blank=True)
    dinner_plate_order = models.ManyToManyField(DinnerPlateOrder, blank=True)
