from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class OrderStatus(models.TextChoices):
    PROCESSING = 'processing', _('В обробці')
    SHIPPED = 'shipped', _('Відправлено')
    DELIVERED = 'delivered', _('Доставлено')
    CANCELLED = 'cancelled', _('Скасовано')

class PaymentStatus(models.TextChoices):
    PENDING = 'pending', _('Очікує оплати')
    PROCESSING = 'processing', _('В процесі')
    COMPLETED = 'completed', _('Оплачено')
    FAILED = 'failed', _('Помилка оплати')

class Order(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Клієнт'))
    delivery_address = models.ForeignKey('user_management.DeliveryAddress', on_delete=models.CASCADE, verbose_name=_('Адреса доставки'))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Загальна сума'))
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PROCESSING, verbose_name=_('Статус замовлення'))
    payment_method = models.CharField(max_length=50, verbose_name=_('Спосіб оплати'))
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING, verbose_name=_('Статус оплати'))
    ttn = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('ТТН'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Створено'))

    class Meta:
        verbose_name = _('Замовлення')
        verbose_name_plural = _('Замовлення')

    def __str__(self):
        return f"{_('Замовлення')} #{self.id} {_('від')} {self.owner}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey('shop.Book', on_delete=models.PROTECT, verbose_name=_('Книга'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Ціна на момент покупки'))
    amount = models.PositiveIntegerField(default=1, verbose_name=_('Кількість'))

    class Meta:
        verbose_name = _('Товар у замовленні')
        verbose_name_plural = _('Товари в замовленні')

    def __str__(self):
        return f"{self.book.title} ({self.amount} {_('шт.')})"