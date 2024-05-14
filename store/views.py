from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, TemplateView, View, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pizza, Cart, CartItem, Order, OrderItem, ShippingAddress, Payment
from django.http import JsonResponse
from accounts.models import JohnPizzaAbstractUserModel

class IndexView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pizzas'] = Pizza.objects.all()
        return context

class PizzaListView(ListView):
    model = Pizza
    template_name = 'store/pizza_list.html'
    context_object_name = 'pizzas'

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = JohnPizzaAbstractUserModel
    template_name = 'store/dashboard.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

class CustomDashboardView(LoginRequiredMixin, TemplateView):
    model = JohnPizzaAbstractUserModel
    template_name = 'store/dashboard.html'
    context_object_name = 'customer'

class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        pizza_id = request.POST.get('pizza_id')
        pizza = Pizza.objects.get(id=pizza_id)

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, pizza=pizza)
        cart_item.quantity += 1
        cart_item.save()

        return redirect('store:view_cart')

class CartView(ListView):
    model = CartItem
    template_name = 'store/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CartItem.objects.filter(cart__user=self.request.user)

        elif self.request.user.is_anonymous:
            return CartItem.objects.filter(cart__session_key=self.request.session.session_key)

class CartConfirmationView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'store/cart_confirmation.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
    
class CheckoutView(TemplateView):
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.request.user.cart_items.all() if self.request.user.is_authenticated else []
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        context['cart_items'] = cart_items
        context['total_price'] = total_price
        context['shipping_form'] = ShippingForm()
        return context

    def post(self, request):
        shipping_form = ShippingForm(request.POST)

        if shipping_form.is_valid():
            cart_items = request.user.cart_items.all() if request.user.is_authenticated else []
            total_price = sum(item.product.price * item.quantity for item in cart_items)
            order = Order.objects.create(user=request.user if request.user.is_authenticated else None, total_amount=total_price)

            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

            request.user.cart_items.clear() if request.user.is_authenticated else Cart.objects.filter(session_key=request.session.session_key).delete()

            return redirect('store:order_confirmation')

        else:
            # Handle invalid forms
            return render(request, self.template_name, {'shipping_form': shipping_form})

class OrderView(LoginRequiredMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = CartItem.objects.filter(cart__user=self.request.user)
        context['cart_items'] = cart_items
        total_price = sum(item.pizza.price * item.quantity for item in cart_items)
        context['total_price'] = total_price
        return context

    def post(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(cart__user=self.request.user)
        total_amount = 0
        order_items = []

        order = Order.objects.create(
            user=self.request.user,
            total=total_amount,
        )

        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                pizza=cart_item.pizza,
                quantity=cart_item.quantity
            )
            total_amount += cart_item.pizza.price * cart_item.quantity
            order_items.append(order_item)
        order.items.set(order_items)

        cart_items.delete()
        
        cart_queryset = Cart.objects.filter(user=self.request.user)
        cart_queryset.delete()

        return redirect('store:order_confirmation') 

class OrderConfirmationView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'store/order.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_items = OrderItem.objects.filter(order__user=self.request.user)
        context['order_items'] = order_items
        return context

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).last()

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'store/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).all()

class RemoveFromCartView(View):
    def post(self, request):
        cart_item_id = request.POST.get('cart_item_id')
        CartItem.objects.filter(id=cart_item_id).delete()
        return JsonResponse({'success': True})

class UpdateQuantityView(View):
    def post(self, request):
        cart_item_id = request.POST.get('cart_item_id')
        quantity = int(request.POST.get('quantity'))
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({'success': True})

class ShippingAddressView(LoginRequiredMixin, CreateView):
    model = ShippingAddress
    fields = ['address', 'city', 'state', 'zip_code']
    template_name = 'shipping_address.html'

    def form_valid(self, form):
        shipping_address = form.save(commit=False)
        shipping_address.user = self.request.user
        shipping_address.save()
        return redirect('payment')

class PaymentView(LoginRequiredMixin, CreateView):
    model = Payment
    fields = ['payment_method', 'transaction_id']
    template_name = 'payment.html'

    def form_valid(self, form):
        order = Order.objects.filter(user=self.request.user).last()
        payment = form.save(commit=False)
        payment.order = order
        payment.amount = order.total
        payment.payment_status = "Completed"
        payment.save()
        messages.success(self.request, "Payment processed successfully")
        return redirect('order_confirmation')