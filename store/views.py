from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, 
    ListView, 
    TemplateView, 
    View, 
    DetailView,
    UpdateView,
    FormView,
    DeleteView,
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pizza, Cart, CartItem, Order, OrderItem, Coupon
from django.http import JsonResponse
from .forms import CartCheckoutForm, PizzaForm, CouponForm, ApplyCouponForm
from django.contrib.auth import get_user_model

User = get_user_model()


class IndexView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pizzas'] = Pizza.objects.all()
        return context

class PizzaCreateView(CreateView):
    model = Pizza
    template_name = 'store/add_product.html'
    form_class = PizzaForm
    success_url = reverse_lazy('store:index')

class CouponCreateView(CreateView):
    model = Coupon
    template_name = 'store/add_coupon.html'
    form_class = CouponForm
    success_url = reverse_lazy('store:order_list')

class PizzaListView(ListView):
    model = Pizza
    template_name = 'store/pizza_list.html'
    context_object_name = 'pizzas'

class CartView(ListView):
    model = CartItem
    template_name = 'store/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CartItem.objects.filter(cart__user=self.request.user)

        elif self.request.user.is_anonymous:
            return CartItem.objects.filter(cart__session_key=self.request.session.session_key)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_queryset().first().cart if self.get_queryset().exists() else None
        context['cart_id'] = cart
        context['cart_total'] = cart.get_cart_total if cart else 0
        context['form'] = ApplyCouponForm()
        return context

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

class CleanCartView(DeleteView):
    model = Cart
    http_method_names = ['post']
    success_url = reverse_lazy('store:view_cart')
   
    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return Cart.objects.get(user=self.request.user)
        else:
            return Cart.objects.get(session_key=self.request.session.session_key)

    def delete(self, request, *args, **kwargs):
        cart = self.get_object()
        cart.delete()  # Delete the cart itself
        return redirect(self.get_success_url())

class RemoveCartItemView(View):
    success_url = reverse_lazy('store:view_cart')

    def post(self, request, *args, **kwargs):
        cart_id = request.POST.get('item_id')
        cart_item = get_object_or_404(CartItem, id=cart_id)
        cart = cart_item.cart
        cart_item.delete()
        
        if not CartItem.objects.filter(cart=cart).exists():
            cart.delete()

        return redirect(self.success_url)

class CartCheckoutView(LoginRequiredMixin, ListView, FormView):
    template_name = 'store/cart_checkout.html'
    context_object_name = 'cart_items'
    form_class = CartCheckoutForm
    success_url = reverse_lazy('store:order_confirmation')

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = self.get_queryset() 
        cart = self.get_queryset().first().cart if self.get_queryset().exists() else None
        context['cart_id'] = cart
        context['total'] = cart.get_cart_total if cart else 0
        context['couponform'] = ApplyCouponForm()
        return context

    def form_valid(self, form):
        cart = Cart.objects.filter(user=self.request.user).last()
        #promotion = form.cleaned_data['promo_code']
        
        #if promotion:
        #total *= (1 - promotion.discount_percentage / 100)

        order = Order.objects.create(
            user=self.request.user,
            shipping_address=form.cleaned_data['shipping_address'] if form.cleaned_data['is_shipping'] == 'True' else None,
            payment_method=form.cleaned_data['payment_method'],
            observation=form.cleaned_data['observation'],
            is_shipping=form.cleaned_data['is_shipping'],
            total=sum(item.pizza.price * item.quantity for item in cart.items.all())        )   

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                pizza=item.pizza,
                quantity=item.quantity
            )

        cart.items.all().delete()
        cart.delete()
        return super().form_valid(form)

class ApplyCartCouponView(View):
    form_class = ApplyCouponForm
    template_name = 'store/cart.html'
    success_url = reverse_lazy('store:view_cart')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                coupon = Coupon.objects.get(code=code)
            except Coupon.DoesNotExist:
                messages.error(request, 'Coupon does not exist.')
                return redirect('store:view_cart')

            cart = self.get_cart(request)
            if cart:
                cart.coupon = coupon
                cart.save()
                messages.success(request, 'Coupon applied successfully.')
                return redirect(self.success_url)
            else:
                messages.error(request, 'No cart found.')
                return redirect('store:view_cart')

        messages.error(request, 'Invalid form submission.')
        return redirect('store:view_cart')

    def get_cart(self, request):
        user = request.user
        if user.is_authenticated:
            return Cart.objects.filter(user=user).first()
        else:
            return Cart.objects.filter(session_key=request.session.session_key).first()

class OrderConfirmationView(LoginRequiredMixin, TemplateView):
    model = Order
    template_name = 'store/order_confirmation.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_queryset()
        context['order_items'] = OrderItem.objects.filter(order=order)
        return context

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).last()

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'store/order.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['order_items'] = OrderItem.objects.filter(order=order)
        return context

class OrderView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'store/order.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['order_items'] = OrderItem.objects.filter(order=order)
        return context

    def get_object(self):
        return Order.objects.filter(user=self.request.user).first()

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'store/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = self.get_queryset()
        for order in orders:
            order.order_items = OrderItem.objects.filter(order=order)
        context['orders'] = orders
    
        context['coupons'] = Coupon.objects.all()
        
        context['users'] = User.objects.all()

        context['pizzas'] = Pizza.objects.all()


        return context