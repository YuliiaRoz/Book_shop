import stripe
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.db import transaction

from shop.models import Book
from user_management.models import DeliveryAddress
from .cart import Cart
from .models import Order, OrderItem, PaymentStatus
# ініціалізація stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class CartView(TemplateView):
    template_name = 'order/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context


def add_to_cart(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)

    quantity = int(request.POST.get('quantity', 1))
    cart.add(book=book, quantity=quantity)

    return redirect('order:cart_detail')


def remove_from_cart(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)

    cart.remove(book)

    return redirect('order:cart_detail')


def create_checkout_session(request):
    cart = Cart(request)
    line_items = []

    # зберігаємо адресу з форми
    if request.method == 'POST':
        city = request.POST.get('city')
        street = request.POST.get('street')

        address = DeliveryAddress.objects.create(
            owner=request.user,
            city=city,
            street=street
        )
        # зберігаємо під ключем 'checkout_address_id'
        request.session['checkout_address_id'] = address.id

    # формуємо список товарів для stripe
    for item in cart:
        line_items.append({
            'price_data': {
                'currency': 'uah',
                'product_data': {'name': str(item['book'].title), },
                'unit_amount': int(item['price'] * 100),
            },
            'quantity': int(item['quantity']),
        })

    # створення сесії оплати
    success_url = request.build_absolute_uri(reverse('order:payment_success'))
    cancel_url = request.build_absolute_uri(reverse('order:payment_cancel'))

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )

    return redirect(session.url, code=303)


def payment_success(request):
    cart = Cart(request)
    user = request.user
    user_email = user.email if user.is_authenticated else 'test@example.com'

    # дістаємо той самий ключ, що і зберігали
    address_id = request.session.get('checkout_address_id')

    with transaction.atomic():
        # рахуємо загальну суму (total_price)
        total_price = sum(item['price'] * item['quantity'] for item in cart)

        # створюємо запис про замовлення З УСІМА обов'язковими полями
        order = Order.objects.create(
            owner=user,
            delivery_address_id=address_id,
            total_price=total_price,
            payment_method='Stripe (Картка)',
            payment_status=PaymentStatus.COMPLETED
        )

        # зберігаємо кожен товар
        for item in cart:
            OrderItem.objects.create(
                order=order,
                book=item['book'],
                price=item['price'],
                amount=item['quantity']
            )

        cart.clear()

        # очищаємо сесію за правильним ключем
        if 'checkout_address_id' in request.session:
            del request.session['checkout_address_id']

    # відправка листа
    subject = f'Дякуємо за ваше замовлення №{order.id}!'
    message = 'Ваша оплата пройшла успішно. Ми вже пакуємо ваші книги і скоро відправимо їх вам!'

    send_mail(
        subject,
        message,
        'shop@mybookstore.com',
        [user_email],
    )

    return render(request, 'order/payment_success.html')


def payment_cancel(request):
    # якщо оплата скасована
    return render(request, 'order/payment_cancel.html')