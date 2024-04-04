from django.urls import path
from . import views

urlpatterns = [  
  path('', views.PizzaListView.as_view(), name='index'),
  path('add-to-cart/<int:pk>/', views.AddToCartView.as_view(), name='add_cart'),
  path('cart/', views.CartView.as_view(), name='view_cart'),
# path('checkout/', CheckoutView.as_view(), name='checkout'),
# path('shipping-address/', ShippingAddressView.as_view(), name='shipping_address'),
# path('payment/', PaymentView.as_view(), name='payment'),
# path('order-confirmation/', OrderConfirmationView.as_view(), name='order_confirmation'),

]