from django.contrib import admin

from .models import Pizza, OrderItem, Order


admin.site.register(Pizza)
admin.site.register(OrderItem)
admin.site.register(Order)