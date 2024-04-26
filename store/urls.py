from django.urls import path
from . import views


app_name = 'store'

urlpatterns = [  
  path('', views.IndexView.as_view(), name='index'),
  path('pizzas/', views.PizzaListView.as_view(), name='view_pizzas'),
  path('add-to-cart/', views.AddToCartView.as_view(), name='add_cart'),
  path('cart/', views.CartView.as_view(), name='view_cart'),
# path('shipping-address/', ShippingAddressView.as_view(), name='shipping_address'),
# path('payment/', PaymentView.as_view(), name='payment'),
  path('cart-confirmation/', views.CartConfirmationView.as_view(), name='confirm_cart'),
  path('order-confirmation/', views.OrderConfirmationView.as_view(), name='order_confirmation'),
  path('order-list/', views.OrderListView.as_view(), name='order_list'),
]