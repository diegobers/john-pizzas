from .models import CartItem


def cart_items_count(request):
    if request.user.is_authenticated:
        # Calculate total quantity for logged-in user
        cart_items = CartItem.objects.filter(cart__user=request.user)
    else:
        # Calculate total quantity for anonymous user
        cart_items = CartItem.objects.filter(cart__session_id=request.session.session_key)

    cart_items_count = sum(item.quantity for item in cart_items)
    
    return {'cart_items_count': cart_items_count}
