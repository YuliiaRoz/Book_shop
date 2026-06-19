from django.contrib import admin

# Register your models here.
import shop.models

class PublishedAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city')

admin.site.register(shop.models.Publisher)
admin.site.register(shop.models.Book)
admin.site.register(shop.models.Author)
admin.site.register(shop.models.Category)
admin.site.register(shop.models.Rating)