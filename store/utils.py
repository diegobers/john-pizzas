from .models import Cart

def count_cart_items(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_id = request.session.session_key
        cart = Cart.objects.filter(session_id=session_id).first()

    if cart:
        total_items = sum(item.quantity for item in cart_items)
        if total_items:
            return total_items
    return 0