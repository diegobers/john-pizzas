from django.urls import path
from . import views

urlpatterns = [  
  path('', views.IndexView.as_view(), name='index'),
  path('pizzas/', views.PizzaListView.as_view(), name='view_pizzas'),
  path('add-to-cart/', views.AddToCartView.as_view(), name='add_cart'),
  path('cart/', views.CartView.as_view(), name='view_cart'),
# path('checkout/', CheckoutView.as_view(), name='checkout'),
# path('shipping-address/', ShippingAddressView.as_view(), name='shipping_address'),
# path('payment/', PaymentView.as_view(), name='payment'),
# path('order-confirmation/', OrderConfirmationView.as_view(), name='order_confirmation'),

]