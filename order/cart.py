import copy
from decimal import Decimal
from django.conf import settings
from shop.models import Book


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        # ВИПРАВЛЕННЯ 1: Додано "not"
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, book, quantity=1, update_quantity=False):
        book_id = str(book.id)
        if book_id not in self.cart:
            self.cart[book_id] = {'quantity': 0, 'price': str(book.price)}

        # Зазвичай при update_quantity кількість замінюється, а не додається,
        # але для кнопок "Додати в кошик" += працюватиме чудово.
        if update_quantity:
            self.cart[book_id]['quantity'] = quantity
        else:
            self.cart[book_id]['quantity'] += quantity

        self.save()

    # ВИПРАВЛЕННЯ 2: Всі нижче наведені методи тепер мають відступ у 4 пробіли
    # і є повноцінною частиною класу Cart
    def save(self):
        self.session.modified = True

    def remove(self, book):
        book_id = str(book.id)
        if book_id in self.cart:
            # Віднімаємо одну одиницю
            self.cart[book_id]['quantity'] -= 1

            # Якщо після віднімання нічого не залишилося, видаляємо запис
            if self.cart[book_id]['quantity'] <= 0:
                del self.cart[book_id]

            self.save()

    def __iter__(self):
        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in=book_ids)
        cart = copy.deepcopy(self.cart)

        for book in books:
            cart[str(book.id)]['book'] = book

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()