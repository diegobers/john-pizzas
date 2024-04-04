from django.urls import path

from .views import IndexTemplateView, PizzasListView, PizzaDetailView


urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index2'),
    #path('pizzas/', PizzasListView.as_view(), name='pizzas'),
    path('detalhes/<slug:slug>/', PizzaDetailView.as_view(), name='detail'), 

    
]