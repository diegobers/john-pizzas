from django.views.generic import ListView

from .models import JohnPizzaAbstractUserModel


class IndexTemplateView(ListView):
    model = JohnPizzaAbstractUserModel
    template_name = "accounts/dashboard.html"
    context_object_name = 'user'