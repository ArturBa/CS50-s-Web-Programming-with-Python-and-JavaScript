from .models import Order, OrderStatus


def get_user_cart(user_id):
    order_status = OrderStatus.objects.filter(name="cart")
    cart = Order.objects.filter(user_id=user_id, status=order_status).all()[0]
    if cart is None:
        cart = Order.objects.create(user_id=user_id, status=order_status)
        cart.save()

    return cart
