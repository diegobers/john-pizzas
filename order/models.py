from django.db import models


class Pizza(models.Model):
    title = models.TextField(max_length=50)
    content = models.TextField(null=True)
    price = models.DecimalField(null=True, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title