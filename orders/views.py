from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Pizza


class PizzaListView(ListView):
    model = Pizza
    template_name = 'orders/pizzas.html'
    context_object_name = 'pizzas'

class PizzaDetailView(DetailView):
    model = Pizza
    template_name = 'orders/pizza.html'
    context_object_name = 'pizza'

def PizzaSearchView(request):
  queryset_list = Pizza.objects.order_by('-list_date')

  # Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(description__icontains=keywords)

  context = {
    'pizzas': queryset_list,
    'values': request.GET
  }

  return render(request, 'orders/search.html', context)