from django.db import migrations

def create_initial_books(apps, schema_editor):
    Publisher = apps.get_model('shop', 'Publisher')
    Author = apps.get_model('shop', 'Author')
    Category = apps.get_model('shop', 'Category')
    Book = apps.get_model('shop', 'Book')

    # 1. Створюємо видавця (обов'язкове поле для книги)
    pub, _ = Publisher.objects.get_or_create(
        name='Tech Books Publishing',
        defaults={
            'address': '123 Tech Lane',
            'city': 'San Francisco',
            'state_province': 'CA',
            'country': 'USA',
            'website': 'https://techbooks.example.com'
        }
    )

    # 2. Створюємо авторів
    author1, _ = Author.objects.get_or_create(
        name='Eric Matthes',
        defaults={'bio': 'Author of Python Crash Course.'}
    )
    author2, _ = Author.objects.get_or_create(
        name='Robert C. Martin',
        defaults={'bio': 'Uncle Bob, author of Clean Code.'}
    )

    # 3. Створюємо категорії
    cat_python, _ = Category.objects.get_or_create(
        name='Python Development',
        slug='python-development'
    )
    cat_programming, _ = Category.objects.get_or_create(
        name='Programming',
        slug='programming'
    )

    # 4. Створюємо книги та додаємо зв'язки ManyToMany
    if not Book.objects.exists():
        book1 = Book.objects.create(
            title='Python Crash Course',
            price=29.99,
            publisher_year=2019,
            amount=15.00,
            publisher=pub
        )
        book1.author.set([author1])
        book1.category.set([cat_python, cat_programming])

        book2 = Book.objects.create(
            title='Clean Code',
            price=34.50,
            publisher_year=2008,
            amount=10.00,
            publisher=pub
        )
        book2.author.set([author2])
        book2.category.set([cat_programming])


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_books),
    ]