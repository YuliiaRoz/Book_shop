## 1. View: `BookCreateView` та `BookUpdateView` (shop/views.py)
**Issue:** Security / Authorization Vulnerability.

### Оригінальний код:
python
class BookCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_authenticated

### AI Рекомендації:
Критична вразливість доступу: Метод test_func перевіряв лише те, чи користувач авторизований. Це означало, що будь-який зареєстрований покупець міг додавати нові книги в магазин або редагувати існуючі.
Рішення: Замінити перевірку is_authenticated на is_staff (або is_superuser), щоб обмежити доступ виключно для адміністраторів магазину.
Фінальний код:
Python
class BookCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_staff and self.request.user.is_active

### 2. View: async_book_list (shop/views.py)
Issue: Data Context Bug / SynchronousOnlyOperation Crash.

Оригінальний код:
Python
    books_list = [book async for book in page_obj.object_list]

    context = {
        'books': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
    }
AI Рекомендації:
Невикористані дані: Логіка успішно асинхронно "розпаковувала" QuerySet у змінну books_list, але у context передавався оригінальний лінивий QuerySet (page_obj.object_list).

Коли HTML-шаблон намагався його відрендерити, Django намагався зробити синхронний запит до БД з асинхронного потоку, що викликало SynchronousOnlyOperation.
Рішення: Передавати в контекст вже готову, асинхронно сформовану змінну books_list.

Фінальний код:
Python
    books_list = [book async for book in page_obj.object_list]
    context = {
        'books': books_list,  # Виправлено
        'page_obj': page_obj,
        'categories': categories,
    }

## 3. View: `create_checkout_session` (order/views.py)
**Issue:** Security (Data Integrity, HTTP Methods, Stale Pricing).

### Оригінальний код:

def create_checkout_session(request):
    cart = Cart(request)
    line_items = []

    if request.method == 'POST':
        address = DeliveryAddress.objects.create(owner=request.user, ...)
    
    for item in cart:
        line_items.append({
            # ...
            'unit_amount': int(item['price'] * 100),
        })
AI Рекомендації:
Missing Authentication: Не було перевірки на авторизацію. Анонімний користувач міг викликати цю функцію, що призвело б до помилки при спробі прив'язати request.user (AnonymousUser) до DeliveryAddress.
Idempotency / HTTP Methods: Функція дозволяла створювати Stripe-сесію через GET запит. Це могло призвести до дублювання сесій при оновленні сторінки.
Pricing Vulnerability: Вартість товару (item['price']) бралася прямо з сесії кошика. Якщо ціна на книгу змінилася в базі даних після того, як користувач додав її до кошика (або якщо сесія була змінена зловмисником), покупець міг заплатити неактуальну ціну.

Рішення: Додати декоратори @login_required та @require_POST. Завжди брати ціну (book.price) безпосередньо з об'єкта бази даних перед генерацією Stripe-сесії.
Фінальний код:
Python
@login_required
@require_POST
def create_checkout_session(request):
    cart = Cart(request)
    # ...
    for item in cart:
        actual_price = item['book'].price  # SECURITY: Always fetch fresh price from DB
        # ...