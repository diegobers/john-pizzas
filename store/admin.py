from django.contrib import admin

from .models import Pizza, Cart, CartItem, Order


admin.site.register(Pizza)
admin.site.register(Order)
admin.site.register(Cart)
