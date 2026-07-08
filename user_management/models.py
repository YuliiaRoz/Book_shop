from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from shop.models import Book


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11)

    def __str__(self):
        return self.username

class DeliveryAddress(models.Model):
    post_service = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    branch = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class LastView(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)