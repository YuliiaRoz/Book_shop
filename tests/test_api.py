import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from shop.models import Category


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db, django_user_model):
    return django_user_model.objects.create_user(username='test_user', email='user@test.com', password='password123')


@pytest.fixture
def admin_user(db, django_user_model):
    return django_user_model.objects.create_superuser(username='admin',email='admin@test.com', password='password123')


@pytest.fixture
def auth_client(test_user):
    client =APIClient()
    client.force_authenticate(user=test_user)
    return client


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


#ТЕСТИ ДОСТУПНОСТІ
@pytest.mark.django_db
@pytest.mark.parametrize("url, expected_status", [
    ('/api/books/', 200),
    ('/api/categories/', 200),
    ('/api/docs/', 200),
    ('/api/orders/', 401),  # Захищено
    ('/api/carts/', 401),  # Захищено
])
def test_public_and_protected_endpoints(api_client, url, expected_status):
    response = api_client.get(url)
    assert response.status_code == expected_status


#ТЕСТИ АВТОРИЗАЦІЇ
@pytest.mark.django_db
@pytest.mark.parametrize("url", [
    '/api/orders/',
    '/api/carts/'
])
def test_endpoints_allow_authenticated(auth_client, url):
    response = auth_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_jwt_token_obtain(api_client, test_user):
    response = api_client.post('/api/token/', {'username': 'test_user', 'password': 'password123'})
    assert response.status_code == 200
    assert 'access' in response.data


@pytest.mark.django_db
def test_jwt_token_invalid(api_client):
    response = api_client.post('/api/token/', {'username': 'wrong', 'password': '123'})
    assert response.status_code == 401


#ТЕСТИ ПРАВ АДМІНІСТРАТОРА
@pytest.mark.django_db
@pytest.mark.parametrize("method, url, data, expected_user_status, expected_admin_status", [
    ('post', '/api/categories/', {'name': 'New', 'slug': 'new'}, 403, 201),
    ('delete', '/api/categories/999/', {}, 403, 404),  # 404 бо категорії 999 немає, але адміна пустило
    ('post', '/api/books/', {'title': 'New Book', 'price': 100}, 403, 400),  # 400 бо бракує полів, але пустило
    ('delete', '/api/books/999/', {}, 403, 404),
])
def test_admin_permissions(api_client, auth_client, admin_client, method, url, data, expected_user_status,
                           expected_admin_status):
    # Звичайний юзер отримує 403 Forbidden
    user_func = getattr(auth_client, method)
    assert user_func(url, data).status_code == expected_user_status

    # Адмін проходить перевірку (отримує 201, 400 або 404)
    admin_func = getattr(admin_client, method)
    assert admin_func(url, data).status_code == expected_admin_status


#ТЕСТИ КОШИКА (4 тести)
@pytest.mark.django_db
@pytest.mark.parametrize("action, data, expected_status", [
    ('get', {}, 200),
    ('post', {'book_id': 999, 'quantity': 1}, 404),  # Книги не існує
])
def test_cart_operations(auth_client, action, data, expected_status):
    func = getattr(auth_client, action)
    response = func('/api/carts/', data)
    assert response.status_code == expected_status


@pytest.mark.django_db
def test_cart_unauthorized_post(api_client):
    assert api_client.post('/api/carts/', {}).status_code == 401


@pytest.mark.django_db
def test_cart_unauthorized_get(api_client):
    assert api_client.get('/api/carts/').status_code == 401


# === 5. ТЕСТИ ФІЛЬТРАЦІЇ КНИГ (4 тести) ===
@pytest.mark.django_db
@pytest.mark.parametrize("query_params", [
    '?search=Harry',
    '?ordering=price',
    '?ordering=-price',
    '?category__slug=fiction',
])
def test_book_filters(api_client, query_params):
    response = api_client.get(f'/api/books/{query_params}')
    assert response.status_code == 200