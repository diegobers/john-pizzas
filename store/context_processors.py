#from .models import CartItem
#
#
#def cart_items_count(request):
#    if request.user.is_authenticated:
#        # Retrieve cart items for logged-in user
#        cart_items = CartItem.objects.filter(cart__user=request.user, cart__session_id=request.session.session_key)
#    else:
#        # Retrieve cart items for anonymous user (by session ID or any other identifier)
#        cart_items = CartItem.objects.filter(cart__session_id=request.session.session_key)
#
#    cart_items_count = sum(item.quantity for item in cart_items)
#    
#    return {'cart_items_count': cart_items_count}


