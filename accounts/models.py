from django.db import models
from django.contrib.auth.models import AbstractUser


class JohnPizzaAbstractUserModel(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
