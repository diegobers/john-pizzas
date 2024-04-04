from django.contrib.auth.models import AnonymousUser
from .models import CartItem


def cart_items_count(request):
    if isinstance(request.user, AnonymousUser):
        # Calculate total quantity for anonymous user
        cart_items = CartItem.objects.all()
    else:
        # Calculate total quantity for logged-in user
        cart_items = CartItem.objects.filter(cart__user=request.user)


    cart_items_count = sum(item.quantity for item in cart_items)
    
    return {'cart_items_count': cart_items_count}



