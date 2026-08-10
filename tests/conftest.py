import pytest
import factory
from django.contrib.auth import get_user_model
from shop.models import Book, Category, Author, Publisher

User = get_user_model()

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    name = factory.Faker('word')
    slug = factory.Faker('slug')

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
    name = factory.Faker('name')

class PublisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publisher
    name = factory.Faker('company')

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=3)
    price = 450.00
    amount = 18
    available = True
    publisher = factory.SubFactory(PublisherFactory)
    publisher_year = 2026

@factory.post_generation
def category(self, create, extracted, **kwargs):
    if not create: return
    if extracted:
        for category in extracted: self.category.add(category)

@factory.post_generation
def author(self, create, extracted, **kwargs):
    if not create: return
    if extracted:
        for author in extracted: self.author.add(author)


@pytest.fixture(autouse=True)
def disable_debug_toolbar(settings):
    settings.DEBUG = False
    settings.MIDDLEWARE = [m for m in settings.MIDDLEWARE if 'debug_toolbar' not in m]

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='test_user', password='password123')

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(username='admin', password='password123')

@pytest.fixture
def test_category(db):
    return Category.objects.create(name='Fantasy', slug='fantasy')

@pytest.fixture
def test_author(db):
    return Author.objects.create(name='J.K. Rowling')

@pytest.fixture
def test_publisher(db):
    return Publisher.objects.create(name='Test Publisher')

@pytest.fixture
def test_book(db, test_category, test_author, test_publisher):
    book = Book.objects.create(
        title='Harry Potter',
        price=450.00,
        amount=18,
        available=True,
        publisher=test_publisher,
        publisher_year=2026
    )
    book.category.add(test_category)
    book.author.add(test_author)
    return book