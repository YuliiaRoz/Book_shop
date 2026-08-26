from rest_framework import serializers
from .models import Order, OrderItem
from shop.models import Book

class OrderSerializer(serializers.ModelSerializer):
    book_title = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'book_title', 'price', 'amount']

class OrderItemSerializer(serializers.ModelSerializer):
    items = OrderSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'owner', 'delivery_address', 'total_price', 'status', 'payment_status', 'payment_method', 'created', 'items']
