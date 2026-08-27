from rest_framework import serializers
from .models import Order, OrderItem
from shop.models import Book

class OrderItemSerializer(serializers.ModelSerializer):
    book_title = serializers.SerializerMethodField(source='book_title')
    author_name = serializers.SerializerMethodField(source='book.author_name')

    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'book_title', 'author_name', 'price', 'amount']
    def get_author_name(self, obj):
        return ", ".join([book.author_name for book in obj.books.all()])

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'owner', 'delivery_address', 'total_price', 'status', 'payment_status', 'payment_method', 'created', 'items']
