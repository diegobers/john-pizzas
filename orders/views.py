from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404

from django.views import  View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Pizza, OrderItem, Order


class OrdersListView(ListView):
    model = Order
    template_name = 'orders/orders.html'
    context_object_name = 'orders'

class OrderItemListView(DetailView):
    model = OrderItem
    template_name = 'orders/order-itens.html'
    context_object_name = 'order_item'

class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'orders/order-summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Carrinho vazio!!")
            return redirect("/")

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
  return orders

def add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":

        order_key = request.POST.get("order_key")
        user_id = request.user.id
        baskettotal = basket.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user_id=user_id,
                full_name="name",
                address1="add1",
                address2="add2",
                total_paid=baskettotal,
                order_key=order_key,
            )
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(
                    order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"]
                )

        response = JsonResponse({"success": "Return something"})
        return response


#def product_all(request):
#    products = Product.objects.prefetch_related("product_image").filter(is_active=True)
#    return render(request, "catalogue/index.html", {"products": products})
#def category_list(request, category_slug=None):
#    category = get_object_or_404(Category, slug=category_slug)
#    products = Product.objects.filter(
#        category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True)
#    )
#    return render(request, "catalogue/category.html", {"category": category, "products": products})
#def product_detail(request, slug):
#    product = get_object_or_404(Product, slug=slug, is_active=True)
#    return render(request, "catalogue/single.html", {"product": product})
#def payment_confirmation(data):
#    Order.objects.filter(order_key=data).update(billing_status=Tru
#def user_orders(request):
#    user_id = request.user.id
#    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
#  