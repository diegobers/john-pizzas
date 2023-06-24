from django.shortcuts import render

from orders.models import Pizza


def index(request):
    pizzas = Pizza.objects.order_by('-list_date').filter(is_published=True)[:3]

    context = {
        'pizzas': pizzas, 
    }

    return render(request, 'pages/index.html', context)