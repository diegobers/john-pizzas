from django.db import models
from django.contrib.auth.models import AbstractUser


class JohnPizzaAbstractUserModel(AbstractUser):
    phone_number = models.CharField(max_length=5, blank=True)
    address = models.CharField(max_length=12, blank=True)
    photo = models.ImageField(upload_to='user/', default='/user/profile.png')
