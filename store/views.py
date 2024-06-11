from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import (
    CreateView, 
    ListView, 
    TemplateView, 
    View, 
    DetailView,
    FormView,
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pizza, Cart, CartItem, Order, OrderItem
from django.http import JsonResponse
from .forms import CartCheckoutForm, PizzaForm


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
    
    #def get_queryset(self):
    #    if self.request.user.is_authenticated:
    #        return CartItem.objects.filter(cart__user=self.request.user)
    #    else:
    #        session_key = self.request.session.session_key
    #        if not session_key:
    #            self.request.session.save()  # Ensure the session is saved and has a session key
    #            session_key = self.request.session.session_key
    #        return CartItem.objects.filter(cart__session_key=session_key)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_queryset().first().cart if self.get_queryset().exists() else None
        context['cart_total'] = cart.get_cart_total if cart else 0
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
        return context

    def form_valid(self, form):
        cart = Cart.objects.filter(user=self.request.user).last()
        #promotion = form.cleaned_data['promo_code']
        total = sum(item.pizza.price * item.quantity for item in cart.items.all())
        
        #if promotion:
        #total *= (1 - promotion.discount_percentage / 100)

        order = Order.objects.create(
            user=self.request.user,
            shipping_address=form.cleaned_data['shipping_address'] if form.cleaned_data['is_shipping'] == 'True' else None,
            payment_method=form.cleaned_data['payment_method'],
            observation=form.cleaned_data['observation'],
            is_shipping=form.cleaned_data['is_shipping'] == 'True',
            total=total
        )   

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                pizza=item.pizza,
                quantity=item.quantity
            )

        cart.items.all().delete()
        return super().form_valid(form)

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "Cupom Inválido!")
        return redirect("store:view_cart")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("store:view_cart")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("store:view_cart")

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
        return context


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