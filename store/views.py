from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pizza, Cart, CartItem, Order, ShippingAddress, Payment
from .utils import count_cart_items
from django.http import JsonResponse


class PizzaListView(ListView):
    model = Pizza
    template_name = 'store/pizza_list.html'
    context_object_name = 'pizzas'

class AddToCartView(CreateView):
    model = CartItem
    fields = ['quantity']
    template_name = 'add_to_cart.html'

    def form_valid(self, form):
        pizza_id = self.kwargs['pk']
        pizza = Pizza.objects.get(pk=pizza_id)
        quantity = form.cleaned_data['quantity']

        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            session_id = self.request.session.session_key
            cart, created = Cart.objects.get_or_create(session_id=session_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, pizza=pizza)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        
        messages.success(self.request, "Item added to cart")
        return redirect('index')

class CartView(ListView):
    model = CartItem
    template_name = 'store/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
        else:
            session_id = self.request.session.session_key
            cart = Cart.objects.filter(session_id=session_id).first()
        if cart:
            return cart.items.all()
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = sum(item.subtotal() for item in context['cart_items'])
        context['total_qty'] = sum(item.quantity for item in context['cart_items'])

        return context

class CheckoutView(LoginRequiredMixin, CreateView):
    model = Order
    fields = []
    template_name = 'checkout.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=self.request.user)[0]
        else:
            cart = Cart.objects.get_or_create(session_id=self.request.session.session_key)[0]
        order = form.save(commit=False)
        order.user = self.request.user
        order.total = sum(item.subtotal() for item in cart.items.all())
        order.save()
        order.items.set(cart.items.all())
        cart.items.clear()
        messages.success(self.request, "Order placed successfully")
        return redirect('shipping_address')

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

class OrderConfirmationView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_confirmation.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).last()