from django.shortcuts import render
from django.views.generic.list import ListView

from order.models import Pizza


class IndexView(ListView):
    model = Pizza
    template_name = 'index/index.html'
    context_object_name = 'pizzas'