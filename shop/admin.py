from django.contrib import admin
from shop.models import Category, Book, Author, Rating, Publisher
# Register your models here.
import shop.models


class BookInline(admin.StackedInline):
    model = Book
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'available', 'amount')
    list_filter = ('category', 'author')
    search_fields = ('title', )

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'city','website')
    inlines = [BookInline]

def display_category(self, obj):
    return ", ".join([str(cat) for cat in obj.category.all()])
display_category.short_description = "Category"

admin.site.register(Rating)
admin.site.register(Author)
