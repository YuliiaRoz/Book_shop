from django.urls import path
from shop.views import (
    async_book_list,
    async_book_detail,
    async_book_delete,
    BookCreateView,
    BookUpdateView,
    custom_404_view
)

app_name = 'shop'

urlpatterns = [
    path('', async_book_list, name='book_list'),
    path('books/<int:pk>', async_book_detail, name='book_detail'),
    path('books/add', BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', async_book_delete, name='book_delete'),
]