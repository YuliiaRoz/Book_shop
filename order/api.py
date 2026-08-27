from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from .serializers import OrderSerializer
from shop.models import Book
from .cart import Cart
from shop.permissions import IsOwnerOrReadOnly

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        if user.is_authenticated:
            return Order.objects.filter(owner=user)
        return Order.objects.none()

    def perform_create(self, serializer):
        order = serializer.save(owner=self.request.user)
        cart = Cart(self.request)

        for item in cart:
            OrderItem.objects.create(
                order=order,
                book=item['book'],
                price=item['price'],
                amount=item['quantity']
            )

            cart.clear()

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        cart = Cart(request)
        cart_items = list(cart)
        total = sum(item['price'] * item['quantity'] for item in cart)
        return Response({'item': cart_items, 'total_price': total})

    def create(self, request):
        cart = Cart(request)
        book_id = request.data.get('book_id')
        quantity = int(request.data.get('quantity', 1))

        book = get_object_or_404(Book, id=book_id)
        cart.add(book=book, quantity=quantity)

        return Response({'status': 'Book added to cart'}, status=status.HTTP_201_CREATED)