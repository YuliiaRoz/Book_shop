from django.db import migrations

def create_initial_books(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    Book = apps.get_model('shop', 'Book')

    # Створюємо базові категорії, якщо їх ще немає
    cat_python, _ = Category.objects.get_or_create(
        name='Python Development', 
        slug='python-development'
    )
    cat_fiction, _ = Category.objects.get_or_create(
        name='Fiction', 
        slug='fiction'
    )

    # Створюємо тестові книги, якщо таблиця книг порожня
    if not Book.objects.exists():
        Book.objects.create(
            title='Python Crash Course',
            slug='python-crash-course',
            description='A hands-on, project-based introduction to programming with Python.',
            price=29.99,
            category=cat_python,
            stock=15
        )
        Book.objects.create(
            title='Clean Code',
            slug='clean-code',
            description='A Handbook of Agile Software Craftsmanship.',
            price=34.50,
            category=cat_python,
            stock=10
        )
        Book.objects.create(
            title='The Master and Margarita',
            slug='the-master-and-margarita',
            description='A classic novel by Mikhail Bulgakov.',
            price=19.99,
            category=cat_fiction,
            stock=8
        )

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),  # Замініть на номер вашої останньої міграції в додатку shop, якщо потрібно
    ]

    operations = [
        migrations.RunPython(create_initial_books),
    ]