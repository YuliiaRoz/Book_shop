from django.contrib import admin
from order.models import Order, OrderDetail

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'status', 'payment_method', 'payment_status',)
    search_fields = ('owner',)
    list_filter = ('status', 'payment_method',)

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order__id', 'book', 'amount', 'price', 'order_owner',)
    search_fields = ('order', 'book',)
    list_filter = ('order',)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail)
