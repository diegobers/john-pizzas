from django.urls import path

from .views import IndexTemplateView, PizzasListView


urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('pizzas/', PizzasListView.as_view(), name='pizzas'),

    
]