from django.db import models
from django.conf import settings


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    photo_main = models.ImageField(upload_to='product/', default='/product/pizza.jpeg')

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

class Order(models.Model):
    ORDER_STATUS  = [
        ('received','Recebido'),
        ('inprogress','Preparando'),
        ('delivered','Entregue'),
        ('canceled','Cancelado'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash','Dinheiro'),
        ('card','Cartão'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    observation = models.TextField(blank=True, null=True)
    is_shipping = models.BooleanField(default=False)
    shipping_address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='card')
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='received')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()