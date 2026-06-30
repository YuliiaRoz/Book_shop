from django.db import models

# Create your models here.
class OrderDetail(models.Model):
    book = models.ForeignKey('shop.Book', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField()
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order.id}, {self.book.title}, {self.amount}'

class OrderStatus(models.Model):
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

class PaymentStatus(models.Model):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'

class Order(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    delivery_address = models.ForeignKey('user_management.DeliveryAddress', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20)
    payment_status = models.CharField(max_length=20)
    ttn = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.id}, {self.id}'