from django.shortcuts import render

import shop.models

# Create your views here.
def main_page(request):
    result = shop.models.Book.objects.all()

    author = shop.models.Author.objects.get(pk=1)
    result = shop.models.Book.objects.filter(author=author)

    new_author = shop.models.Author(name = 'A1')
    new_author.bio = 'A1 bio'
    new_author.save()

    
    return ''