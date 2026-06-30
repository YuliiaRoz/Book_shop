from django.db import models

# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state_province = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    website = models.URLField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(Author)
    category = models.ManyToManyField(Category)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)
    publisher_year = models.IntegerField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    calculated_average = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    def __str__(self):
        return self.title

class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    rating = models.IntegerField()
    feedback = models.TextField()
