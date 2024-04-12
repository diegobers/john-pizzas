from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, TemplateView, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pizza, Cart, CartItem, Order, ShippingAddress, Payment
#from .utils import count_cart_items
from django.http import JsonResponse
from django.contrib.sessions.backends.db import SessionStore


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
 

class CartView(ListView):
    model = CartItem
    template_name = 'store/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CartItem.objects.filter(cart__user=self.request.user)

        if self.request.user.is_anonymous:
            if self.request.session.session_key:
                return CartItem.objects.filter(cart__session_key=self.request.session.session_key)
        else:
            return redirect('store:view_cart') 

class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        pizza_id = request.POST.get('pizza_id')
        qty = int(request.POST.get('quantity', 1))
        pizza = Piiza.objects.get(id=pizza_id)

        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        
        if request.user.is_anonymous:
            if request.session.session_key:
                cart = Cart.objects.get(session_key=request.session.session_key)
            else:
                session_store = SessionStore()
                session_store.save()
                session_key = session_store.session_key
                
                request.session = session_store
                cart = Cart.objects.create(session_key=session_store.session_key) 
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, pizza=pizza, quantity=qty)
        cart_item.save()

        return redirect('store:view_cart')

class CartView111(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(cart__user=request.user)
        else:
            session_key = request.session.session_key
            cart_items = CartItem.objects.filter(cart__session_key=session_key)
        
        return render(request, 'store/cart.html', {'cart_items': cart_items})


class AddToCartView111(View):
    def post(self, request):
        pizza_id = request.POST.get('pizza_id')
        qty = int(request.POST.get('quantity', 1))
        pizza = Pizza.objects.get(id=pizza_id)

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        
        if request.user.is_anonymous:
            if request.session.session_key:
                cart = Cart.objects.get(session_key=request.session.session_key)
            else:
                session_store = SessionStore()
                session_store.save()
                session_key = session_store.session_key
                request.session = session_store
                cart = Cart.objects.create(session_key=session_store.session_key) 
        
        cart_item = CartItem.objects.create(cart=cart, pizza=pizza, quantity=qty)
        cart_item.save()

        return redirect('view_cart')

class AddToCartView2(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = Product.objects.get(pk=product_id)

        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({'success': True})

class AddToCartView3(CreateView):
    model = CartItem
    fields = ['quantity']
    template_name = 'add_to_cart.html'

    def form_valid(self, form):
        pizza_id = self.kwargs['pk']
        pizza = Pizza.objects.get(pk=pizza_id)
        quantity = form.cleaned_data['quantity']

        if self.request.user.is_authenticated:
            session_key = self.request.session.session_key
            cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            session_key = self.request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, pizza=pizza)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        
        messages.success(self.request, "Item added to cart")
        return redirect('index')

class CartView1(ListView):
    model = CartItem
    template_name = 'store/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        print(self.request.session)
        print('*********AAAA******************************')
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
        else:
            session_key = self.request.session.session_key
            cart = Cart.objects.filter(session_key=session_key).first()
        if cart:
            return cart.items.all()
        print(self.request)
        print('***************************************')
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['total'] = sum(item.subtotal() for item in context['cart_items'])
        context['total_qty'] = sum(item.quantity for item in context['cart_items'])

        return context



class RemoveFromCartView(View):
    def post(self, request):
        cart_item_id = request.POST.get('cart_item_id')
        CartItem.objects.filter(id=cart_item_id).delete()
        return JsonResponse({'success': True})



class CheckoutView(LoginRequiredMixin, CreateView):
    model = Order
    fields = []
    template_name = 'checkout.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=self.request.user)[0]
        else:
            cart = Cart.objects.get_or_create(session_key=self.request.session.session_key)[0]
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