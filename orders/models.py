from django.db import models
from django.conf import settings

from django.utils.translation import gettext_lazy as _

#from cart.models import CartItem


class Pizza(models.Model):
    class CategoryChoices(models.TextChoices):
        DOCE = "Doce"
        SALGADA = "Salgada"     
    category = models.CharField(
        choices=CategoryChoices.choices, 
        max_length=7, 
        default=CategoryChoices.SALGADA
    )
    description = models.TextField()
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    slug = models.SlugField()
    photo_1 = models.ImageField(upload_to='product/', default='/product/pizza.jpeg')
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.description
        

class Order(models.Model):
    #customer = models.ForeignKey(
    #    settings.AUTH_USER_MODEL, 
    #    on_delete=models.CASCADE
    #)
#   ref_code = models.CharField(max_length=20, blank=True, null=True)
    #items = models.ManyToManyField(CartItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    def __str__(self):
        return self.received

    def get_total(self):
        total = 0
        for order_item in self.items.all():
           total += order_item.get_total_item_price()
        return total

#       if self.coupon:
#           total -= self.coupon.amount