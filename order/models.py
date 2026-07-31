from django.db import models
from django.conf import settings

class OrderStatus(models.TextChoices):
    PROCESSING = 'processing', 'В обробці'
    SHIPPED = 'shipped', 'Відправлено'
    DELIVERED = 'delivered', 'Доставлено'
    CANCELLED = 'cancelled', 'Скасовано'

class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Очікує оплати'
    PROCESSING = 'processing', 'В процесі'
    COMPLETED = 'completed', 'Оплачено'
    FAILED = 'failed', 'Помилка оплати'

class Order(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Клієнт')
    delivery_address = models.ForeignKey('user_management.DeliveryAddress', on_delete=models.CASCADE, verbose_name='Адреса доставки')

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Загальна сума')

    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PROCESSING, verbose_name='Статус замовлення')
    payment_method = models.CharField(max_length=50, verbose_name='Спосіб оплати')
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING, verbose_name='Статус оплати')

    ttn = models.CharField(max_length=50, blank=True, null=True, verbose_name='ТТН')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Створено')

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    def __str__(self):
        return f'Замовлення #{self.id} від {self.owner}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey('shop.Book', on_delete=models.PROTECT, verbose_name='Книга')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна на момент покупки')
    amount = models.PositiveIntegerField(default=1, verbose_name='Кількість')

    class Meta:
        verbose_name = 'Товар у замовленні'
        verbose_name_plural = 'Товари в замовленні'

    def __str__(self):
        return f'{self.book.title} ({self.amount} шт.)'