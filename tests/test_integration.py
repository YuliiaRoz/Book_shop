from unittest.mock import patch
import pytest
from django.urls import reverse
from shop.models import Book
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db
User = get_user_model()


def test_flow_login_success(client, test_user):
    url = reverse('user_management:login')
    response = client.post(url, {'username': 'test_user', 'password': 'password123'})
    assert str(test_user.id) == client.session.get('_auth_user_id')


def test_flow_login_fail(client, test_user):
    url = reverse('user_management:login')
    response = client.post(url, {'username': 'test_user', 'password': 'wrong'})
    assert '_auth_user_id' not in client.session


def test_flow_search_by_title(client, test_book):
    url = reverse('shop:book_list')
    response = client.get(url, {'query': 'Harry'})
    assert test_book in response.context['books']


def test_flow_search_by_author(client, test_book):
    url = reverse('shop:book_list')
    response = client.get(url, {'query': 'J.K. Rowling'})
    assert test_book in response.context['books']


def test_flow_search_by_category(client, test_book, test_category):
    url = reverse('shop:book_list')
    response = client.get(url, {'category': test_category.slug})
    assert test_book in response.context['books']


def test_flow_search_no_results(client, test_book):
    url = reverse('shop:book_list')
    response = client.get(url, {'query': 'Hobbit'})
    assert test_book not in response.context['books']


def test_flow_add_to_cart(client, test_book):
    url = reverse('order:add_to_cart', args=[test_book.id])
    response = client.post(url, {'quantity': 1})
    assert str(test_book.id) in client.session.get('cart', {})


def test_flow_cart_update_quantity(client, test_book):
    url_add = reverse('order:add_to_cart', args=[test_book.id])
    client.post(url_add, {'quantity': 1})
    client.post(url_add, {'quantity': 2, 'update': True})
    cart = client.session['cart']
    assert cart[str(test_book.id)]['quantity'] == 3


def test_flow_remove_from_cart(client, test_book):
    url_add = reverse('order:add_to_cart', args=[test_book.id])
    url_remove = reverse('order:remove_from_cart', args=[test_book.id])
    client.post(url_add, {'quantity': 1})
    client.post(url_remove)
    cart = client.session.get('cart')
    assert str(test_book.id) not in cart


def test_flow_cart_clear(client, test_book):
    client.post(reverse('order:add_to_cart', args=[test_book.id]), {'quantity': 1})
    client.post(reverse('order:remove_from_cart', args=[test_book.id]))
    assert not client.session.get('cart')


def test_flow_admin_create_book(client, admin_user, test_category, test_author, test_publisher):
    client.force_login(admin_user)
    url = reverse('shop:book_create')
    data = {
        'title': 'New Admin Book',
        'category': [test_category.id],
        'author': [test_author.id],
        'publisher': test_publisher.id,
        'price': 450,
        'amount': 1,
        'available': True,
        'publisher_year': 2020
    }

    response = client.post(url, data)
    assert response.status_code == 302


def test_flow_admin_update_book(client, admin_user, test_book, test_publisher, test_author):
    client.force_login(admin_user)
    url = reverse('shop:book_update', args=[test_book.id])
    data = {
        'title': 'Updated Book',
        'category': [cat.id for cat in test_book.category.all()],
        'author': [auth.id for auth in test_book.author.all()],
        'price': 450,
        'amount': 10,
        'available': True,
        'publisher': test_publisher.id,
        'publisher_year': 2026
    }
    client.post(url, data)
    test_book.refresh_from_db()
    assert test_book.title == 'Updated Book'
    assert test_book.price == 450


def test_flow_admin_delete_book(client, admin_user, test_book):
    client.force_login(admin_user)
    url = reverse('shop:book_delete', args=[test_book.id])
    response = client.post(url)
    assert response.status_code == 302
    assert not Book.objects.filter(id=test_book.id).exists()


@patch('order.views.stripe.checkout.Session.create')
def test_flow_checkout_guest_redirect(mock_stripe, client):
    from django.urls import reverse
    mock_stripe.return_value.url = 'https://fake-stripe-url.com'
    url = reverse('order:create_checkout_session')
    response = client.get(url)
    assert response.status_code in [302, 303, 403]


def test_flow_pagination_second_page(client, test_category, test_publisher):
    from shop.models import Book
    for i in range(5):
        book = Book.objects.create(title=f"Page Book {i}", price=10, amount=10, available=True,
                                   publisher=test_publisher, publisher_year=2020)
        book.category.add(test_category)
    url = reverse('shop:book_list')
    response = client.get(url, {'page': 2})
    assert response.status_code == 200
    assert len(response.context['books']) > 0


def test_flow_view_unavailable_book(client, test_category, test_publisher):
    from shop.models import Book
    hidden_book = Book.objects.create(title="Hidden", price=10, amount=0, available=False, publisher=test_publisher,
                                      publisher_year=2020)
    hidden_book.category.add(test_category)
    url = reverse('shop:book_list')
    response = client.get(url)
    assert hidden_book not in response.context['books']