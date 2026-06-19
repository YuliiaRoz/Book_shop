from django.contrib.auth.models import User
from django.db import models

from shop.models import Book


# Create your models here.
class DeliveryAddress(models.Model):
    post_service = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    branch = models.CharField(max_length=200)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class LastView(models.Model):
    book = models.ForeignKey('shop.Book', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)