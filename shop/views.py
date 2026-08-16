from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from shop.models import Book, Category
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import Http404
from django.core.paginator import Paginator
from asgiref.sync import sync_to_async


@sync_to_async
def get_paginated_books(request, queryset, paginate_by):
    paginator = Paginator(queryset, paginate_by)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


async def async_book_list(request):
    """
        Асинхронне відображення каталогу книг.

        Підтримує пошук за назвою або автором (параметр 'query'),
        фільтрацію за категоріями (параметр 'category') та пагінацію.
        Тільки книги з amount > 0 та available=True відображаються.

        Args:
            request (HttpRequest): Об'єкт вхідного запиту.

        Returns:
            HttpResponse: Відрендерений шаблон 'shop/book_list.html'.
        """
    queryset = Book.objects.filter(amount__gt=0, available=True)
    query = request.GET.get('query')
    category_slug = request.GET.get('category')

    if query:
        clean_query = query.strip()
        queryset = queryset.filter(
            Q(title__icontains=clean_query) |
            Q(author__name__icontains=clean_query)
        ).distinct()

    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)

    queryset = queryset.order_by('-id')

    categories = [cat async for cat in Category.objects.all()]

    page_obj = await get_paginated_books(request, queryset, 3)

    # Витягуємо книги асинхронно
    books_list = [book async for book in page_obj.object_list]

    context = {
        'books': books_list,  # ВИПРАВЛЕНО: передаємо готовий список, а не лінивий QuerySet
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'shop/book_list.html', context)


async def async_book_detail(request, pk):
    """
        Асинхронне відображення деталей конкретної книги.

        Args:
            request (HttpRequest): Об'єкт вхідного запиту.
            pk (int): Primary key (ID) книги.

        Raises:
            Http404: Якщо книга з вказаним ID не існує.

        Returns:
            HttpResponse: Відрендерений шаблон 'shop/book_detail.html'.
        """
    try:
        book = await Book.objects.aget(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Книгу не знайдено")

    return render(request, 'shop/book_detail.html', {'book': book})


class BookCreateView(UserPassesTestMixin, CreateView):
    model = Book
    template_name = 'shop/book_form.html'
    fields = ['title', 'author', 'category', 'price', 'publisher_year', 'amount', 'available', 'publisher']
    success_url = reverse_lazy('shop:book_list')

    def test_func(self):
        # ВИПРАВЛЕНО: Тільки персонал (staff) може додавати книги
        return self.request.user.is_staff and self.request.user.is_active


class BookUpdateView(UserPassesTestMixin, UpdateView):
    model = Book
    template_name = 'shop/book_form.html'  # ВИПРАВЛЕНО: Зайві дужки прибрані
    fields = ['title', 'author', 'category', 'price', 'publisher_year', 'amount', 'available', 'publisher']
    success_url = reverse_lazy('shop:book_list')

    def test_func(self):
        # ВИПРАВЛЕНО: Тільки персонал (staff) може редагувати книги
        return self.request.user.is_staff and self.request.user.is_active


@sync_to_async
def check_delete_permission(user):
    return user.is_authenticated and user.has_perm('shop.delete_book')


async def async_book_delete(request, pk):
    has_permission = await check_delete_permission(request.user)
    if not has_permission:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path())

    try:
        book = await Book.objects.aget(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Книгу не знайдено")

    if request.method == 'POST':
        await book.adelete()
        return redirect('shop:book_list')

    return render(request, 'shop/book_confirm_delete.html', {'book': book, 'object': book})


def custom_404_view(request, exception):
    return render(request, 'shop/error_404.html', status=404)