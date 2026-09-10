import pytest
from django.urls import reverse
from shop.models import Book
from order.models import Order, OrderItem
from user_management.models import DeliveryAddress
from django.core import mail

pytestmark = pytest.mark.django_db

# --- UNIT ТЕСТИ ДЛЯ МОДЕЛЕЙ ---

def test_category_str(test_category):
    assert isinstance(test_category.name, str)


def test_book_str(test_book):
    assert test_book.title in str(test_book)


def test_book_amount_validation(test_book):
    test_book.amount = 0
    test_book.save()
    assert test_book.amount == 0


def test_book_detail_availability():
    book = Book(title='Test', price=200)
    assert book.available is True


def test_order_creation(test_user):
    address = DeliveryAddress.objects.create(owner=test_user, city='Lviv', street='Svobody')
    order = Order.objects.create(owner=test_user, delivery_address=address, payment_method='Card')
    assert str(order.id) in str(order)


def test_order_str(test_user):
    address = DeliveryAddress.objects.create(owner=test_user, city='Lviv', street='Svobody')
    order = Order.objects.create(owner=test_user, delivery_address=address, payment_method='Card')
    assert str(order.id) in str(order)


def test_order_item_calculation(test_user, test_book):
    address = DeliveryAddress.objects.create(owner=test_user, city='Lviv', street='Svobody')
    order = Order.objects.create(owner=test_user, delivery_address=address, payment_method='Card')
    item = OrderItem.objects.create(order=order, book=test_book, price=test_book.price, amount=2)
    assert item.amount == 2
    assert item.price == 450.00


# --- UNIT ТЕСТИ ДЛЯ VIEWS

def test_book_list_view_200(client):
    url = reverse('shop:book_list')
    response = client.get(url)
    assert response.status_code == 200


def test_book_detail_view_200(client, test_book):
    url = reverse('shop:book_detail', args=[test_book.id])
    response = client.get(url)
    assert response.status_code == 200


def test_book_detail_view_404(client):
    url = reverse('shop:book_detail', args=[999])
    response = client.get(url)
    assert response.status_code == 404


def test_book_delete_view_unauthenticated(client, test_book):
    url = reverse('shop:book_delete', args=[test_book.id])
    response = client.get(url)
    assert response.status_code == 302


def test_book_delete_view_admin_get(client, admin_user, test_book):
    client.force_login(admin_user)
    url = reverse('shop:book_delete', args=[test_book.id])
    response = client.get(url)
    assert response.status_code == 200


def test_book_list_pagination_context(client, test_category, test_publisher):
    for i in range(4):
        book = Book.objects.create(title=f"Book {i}", price=100, amount=10, publisher=test_publisher,
                                   publisher_year=2020)
        book.category.add(test_category)

    response = client.get(reverse('shop:book_list'))
    assert 'page_obj' in response.context
    assert len(response.context['books']) == 3


def test_book_create_view_unauthenticated(client):
    url = reverse('shop:book_create')
    response = client.get(url)
    assert response.status_code == 302


def test_book_create_view_authenticated(client, test_user):
    client.force_login(test_user)
    url = reverse('shop:book_create')
    response = client.get(url)
    assert response.status_code == 403


def test_book_create_view_admin(client, admin_user):
    client.force_login(admin_user)
    url = reverse('shop:book_create')
    response = client.get(url)
    assert response.status_code == 200


def test_book_update_view_unauthenticated(client, test_book):
    url = reverse('shop:book_update', args=[test_book.id])
    response = client.get(url)
    assert response.status_code == 302


def test_book_update_view_admin(client, admin_user, test_book):
    client.force_login(admin_user)
    url = reverse('shop:book_update', args=[test_book.id])
    response = client.get(url)
    assert response.status_code == 200


def test_cart_session_initialization(client):
    session = client.session
    assert 'cart' not in session


def test_custom_404_handler(client):
    response = client.get('/non-existent-url-12345/')
    assert response.status_code == 404


def test_email_sending():
    mail.send_mail(
        'Вітаємо у магазині!',
        'Дякуємо за реєстрацію.',
        'noreply@bookshop.com',
        ['user@example.com'],
        fail_silently=False,
    )

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == 'Вітаємо у магазині!'
    assert mail.outbox[0].to == ['user@example.com']


def test_empty_form_invalid():
    from shop.forms import SearchForm
    form = SearchForm(data={'query': 'Harry'})
    assert form.is_valid() is True

    empty_form = SearchForm(data={})
    assert empty_form.is_valid() is True

# AI запропоновані тести
# ==========================================
# ЗГЕНЕРОВАНІ AI ТЕСТИ ДЛЯ МОДЕЛЕЙ
# ==========================================

# Generated with AI, reviewed and modified
def test_publisher_str_and_creation(db):
    from shop.models import Publisher
    publisher = Publisher.objects.create(name="O'Reilly Media")
    initial_count = Publisher.objects.count()

    assert publisher.name == "O'Reilly Media"
    assert str(publisher) == "O'Reilly Media"
    assert Publisher.objects.count() == initial_count + 1


# Generated with AI, reviewed and modified
def test_author_str_and_creation(db):
    from shop.models import Author
    author = Author.objects.create(name="Сергій Жадан")

    assert author.name == "Сергій Жадан"
    assert str(author) == "Сергій Жадан"


# Generated with AI, reviewed and modified
def test_delivery_address_fields(test_user):
    from user_management.models import DeliveryAddress
    address = DeliveryAddress.objects.create(
        owner=test_user,
        city="Київ",
        street="Хрещатик"
    )

    assert address.city == "Київ"
    assert address.street == "Хрещатик"
    assert address.owner.username == test_user.username