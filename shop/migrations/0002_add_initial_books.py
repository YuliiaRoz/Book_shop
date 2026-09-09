from django.db import migrations

def create_initial_books(apps, schema_editor):
    Category = apps.get_model('shop', 'Category')
    Book = apps.get_model('shop', 'Book')

    cat_python, _ = Category.objects.get_or_create(
        name='Python Development',
        slug='python-development'
    )
    cat_fiction, _ = Category.objects.get_or_create(
        name='Fiction',
        slug='fiction'
    )

    if not Book.objects.exists():
        book1 = Book.objects.create(
            title='Python Crash Course',
            slug='python-crash-course',
            description='A hands-on, project-based introduction to programming with Python.',
            price=29.99,
            stock=15
        )

        book1.category.set([cat_python])

        book2 = Book.objects.create(
            title='Clean Code',
            slug='clean-code',
            description='A Handbook of Agile Software Craftsmanship.',
            price=34.50,
            stock=10
        )
        book2.category.set([cat_python])

        book3 = Book.objects.create(
            title='The Master and Margarita',
            slug='the-master-and-margarita',
            description='A classic novel by Mikhail Bulgakov.',
            price=19.99,
            stock=8
        )
        book3.category.set([cat_fiction])

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_books),
    ]