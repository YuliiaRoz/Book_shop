from django.urls import path
from shop.views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView, custom_404_view

app_name = 'shop'

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>', BookDetailView.as_view(), name='book_detail'),
    path('books/add', BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),

]