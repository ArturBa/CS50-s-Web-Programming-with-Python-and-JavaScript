from django.contrib.auth.models import User
from django.db import models


class PizzaType(models.Model):
    """
    Pizza type
    """
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'Pizza type: {self.name}'


class Pizza(models.Model):
    """
    Pizza model
    Has info about price for big and small pizza, pizza type and number of available toppings
    """
    name = models.CharField(max_length=64)
    type = models.ForeignKey(PizzaType, on_delete=models.CASCADE, related_name='pizzas')
    toppings_count = models.IntegerField()
    large_price = models.FloatField()
    small_price = models.FloatField()

    def __str__(self):
        return f'Pizza: {self.type.name}:{self.name} with toppings: {self.toppings_count}'


class Topping(models.Model):
    """
    Topping model
    """
    name = models.CharField(max_length=64, unique=True)

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
    """
    Sub adds on model
    """
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f'Sub add: {self.name}'


class Sub(models.Model):
    """
    Sub model
    Has information about price, extra cheese price and if adds are available
    """
    name = models.CharField(max_length=64, unique=True)
    extra_cheese_price = models.FloatField(default=0.5)
    price_large = models.FloatField(blank=True, null=True)
    price_small = models.FloatField(blank=True, null=True)
    adds_available = models.BooleanField()

    def __str__(self):
        return f'Sub: {self.name}'


class SubsOrder(models.Model):
    """
    Sub order model
    Has information about sub type, adds, size, quantity and if extra cheese was chosen
    """
    sub_id = models.ForeignKey(Sub, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    large = models.BooleanField(default=True)
    extra_cheese = models.BooleanField(default=False)
    adds = models.ManyToManyField(SubAdd, blank=True)


class Salad(models.Model):
    """
    Salad model
    """
    name = models.CharField(max_length=64, unique=True)
    price = models.FloatField()

    def __str__(self):
        return f'Salad: {self.name}'


class SaladOrder(models.Model):
    """
    Salad order model
    Has information about type and number of salad
    """
    salad_id = models.ForeignKey(Salad, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Pasta(models.Model):
    """
    Pasta model
    """
    name = models.CharField(max_length=64, unique=True)
    price = models.FloatField()

    def __str__(self):
        return f'Pasta: {self.name}'


class PastaOrder(models.Model):
    """
    Pasta order model
    Has information about type and number of pastas
    """
    pasta_id = models.ForeignKey(Pasta, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class DinnerPlate(models.Model):
    """
    Dinner plate model
    """
    name = models.CharField(max_length=64, unique=True)
    price_large = models.FloatField()
    price_small = models.FloatField()

    def __str__(self):
        return f'Dinner Plate: {self.name}'


class DinnerPlateOrder(models.Model):
    """
    Dinner player order model
    Has information about dinner player number and type
    """
    dinner_plate_id = models.ForeignKey(DinnerPlate, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    large = models.BooleanField(default=True)


class OrderStatus(models.Model):
    """
    Order status model
    Has information about possible order status
    """
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'Order statutes'

    def __str__(self):
        return f'Order status: {self.name}'


class Order(models.Model):
    """
    Order model
    """
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name="orders")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    creation_date = models.DateField(auto_now_add=True)
    pizza_order = models.ManyToManyField(PizzaOrder, blank=True, related_name='order')
    sub_order = models.ManyToManyField(SubsOrder, blank=True, related_name='order')
    salad_order = models.ManyToManyField(SaladOrder, blank=True, related_name='order')
    pasta_order = models.ManyToManyField(PastaOrder, blank=True, related_name='order')
    dinner_plate_order = models.ManyToManyField(DinnerPlateOrder, blank=True, related_name='order')

    def __str__(self):
        return f'[{self.status.name}] Order by {self.user_id.first_name} from {self.creation_date}'
