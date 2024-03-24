from django.urls import path

from .views import OrdersListView, OrderItemListView, OrderSummaryView


urlpatterns = [  
  path('', OrdersListView.as_view(), name='orders-list'),
  path('pedido-detail/', OrderItemListView.as_view(), name='order-detail'),
  path('pedidos/', OrderSummaryView.as_view(), name='orders-summary'),
  #path('pizzas/', PizzaListView.as_view(), name='pizzas'),

]


#path('add/', views.add, name='add'),
#path('', views.PizzaListView.as_view(), name='pizzas'),   
#path('pesquisa', views.PizzaSearchView, name='search'),
#path("", views.product_all, name="store_home"),
#path("<slug:slug>", views.product_detail, name="product_detail"),
#path("shop/<slug:category_slug>/", views.category_list, name="category_list"),
#path('', views.PizzasListView.as_view(), name='pizzas-list'),
#path('<slug>/', views.PizzaDetailView.as_view(), name='pizza-detail'),
#path('adicionar-carrinho/<slug>/', views.add_to_cart, name='add-to-cart'),
#path('remover-carrinho/<slug>/', views.remove_from_cart, name='remove-from-cart'),