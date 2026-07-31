from django.contrib import admin
from order.models import Order, OrderItem

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['book']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'status', 'payment_status','created', 'total_price']
    search_fields = ['status', 'payment_status', 'created']
    list_filter = ['id', 'ttn']

    inlines = [OrderItemInline]
