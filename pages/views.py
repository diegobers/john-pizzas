from django.views.generic import DetailView
from django.views.generic import ListView

from orders.models import Pizza


class IndexTemplateView(ListView):
    queryset = Pizza.objects.all()
    template_name = "pages/index.html"
    context_object_name = 'pizzas'

class PizzasListView(ListView):
    model = Pizza
    template_name = "orders/pizzas.html"
    context_object_name = 'pizzas'

class PizzaDetailView(DetailView):
    model = Pizza
    template_name = "orders/pizza.html"

