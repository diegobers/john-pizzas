from django.urls import path
from . import views


app_name = 'store'

urlpatterns = [  
  path('', views.IndexView.as_view(), name='index'),
  path('pizzas/', views.PizzaListView.as_view(), name='view_pizzas'),
  path('add-cart/', views.AddToCartView.as_view(), name='add_cart'),
  path('add-pizza/', views.PizzaCreateView.as_view(), name='add_pizza'),
  path('add-coupon/', views.CouponCreateView.as_view(), name='add_coupon'),
  #path('dashboard/', views.UserProfileDetailView.as_view(), name='dashboard'),

  path('add-cart-coupon/', views.ApplyCartCouponView.as_view(), name='apply-coupon'),
  path('cart/', views.CartView.as_view(), name='view_cart'),
  
  path('rm-cart/', views.CleanCartView.as_view(), name='clean_cart'),
  path('rm-item-cart/', views.RemoveCartItemView.as_view(), name='rm_item_cart'),

  path('cart-checkout/', views.CartCheckoutView.as_view(), name='checkout_cart'),
  path('add-checkout-coupon/', views.ApplyCheckoutCouponView.as_view(), name='checkout-coupon'),
  path('add-checkout/', views.AddToCheckoutView.as_view(), name='add_checkout'),
  path('rm-item-cart/', views.RemoveCheckoutItemView.as_view(), name='rm_item_checkout'),
  path('rm-cart/', views.CleanCheckoutView.as_view(), name='clean_checkout'),
  
  path('order/', views.OrderView.as_view(), name='order_view'),
  path('order-detalhes/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
  path('order-confirmation/', views.OrderConfirmationView.as_view(), name='order_confirmation'),
  path('order-list/', views.OrderListView.as_view(), name='order_list'),
# path('shipping-address/', ShippingAddressView.as_view(), name='shipping_address'),
# path('payment/', PaymentView.as_view(), name='payment'),
]