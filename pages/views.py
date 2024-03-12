from django.views.generic import ListView

from catalogue.models import Pizza


class IndexTemplateView(ListView):
    model = Pizza
    template_name = "pages/index.html"
    context_object_name = 'pizzas'