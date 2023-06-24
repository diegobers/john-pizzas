from django.urls import path

from . import views


urlpatterns = [  
  path('', views.PizzaListView.as_view(), name='pizzas'),   
  path('pizza/<int:pk>/', views.PizzaDetailView.as_view(), name='pizza'),
  path('pesquisa', views.PizzaSearchView, name='search'),
]