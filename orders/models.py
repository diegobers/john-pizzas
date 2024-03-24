from django.db import models
from django.conf import settings

from django.utils.translation import gettext_lazy as _


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
    price = models.IntegerField()
    slug = models.SlugField()
    photo_1 = models.ImageField(upload_to='product/', default='/product/pizza.jpeg')
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.description

class OrderItem(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(
        Pizza, 
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{ self.quantity } of { self.item.description }"

    def get_total_item_price(self):
        return self.quantity * self.item.price

#   def get_total_discount_item_price(self):
#      return self.quantity * self.item.discount_price
#       
#   def get_amount_saved(self):
#      return self.get_total_item_price() - self.get_total_discount_item_price()
#       
#   def get_final_price(self):
#       if self.item.discount_price:
#         return self.get_total_discount_item_price()
#     return self.get_total_item_price()

class Order(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
#   ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
           total += order_item.get_total_item_price()
        return total

#       if self.coupon:
#           total -= self.coupon.amount