from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from shop.models import Book, Category
from django.db.models import Q, Count
from django.shortcuts import render

# from django.views.generic import DetailView, CreateView
# from msilib.schema import ListView
# from django.shortcuts import render
# import shop
# from shop.models import Book, Category, Author
# from .forms import SearchForm

# # Create your views here.
# def main_page(request):
#     available_books = Book.objects.filter(amount__gt=0, available=True)
#     categories_with_count = Category.objects.annotate(total_books=Count('book'))
#
#     form = SearchForm(request.GET)
#     search_results = None
#
#     if form.is_valid() and form.cleaned_data.get('query'):
#         search_query = form.cleaned_data['query']
#         search_results = Book.objects.filter(
#         Q(title__icontains=search_query) |Q(author__name__icontains=search_query)
#     ).distinct()
#
#     context = {
#         'available_books': available_books,
#         'search_results': search_results,
#         'categories_with_count': categories_with_count,
#         'form': form,
#     }
#     return render(request, 'shop/base.html', context)

# ListView - виведення списку всіх книг
class BookListView(ListView):
    model = Book
    template_name = 'shop/book_list.html'
    context_object_name = 'books'

    paginate_by = 3

    def get_queryset(self):
        queryset = Book.objects.filter(amount__gt=0, available=True)
        query = self.request.GET.get('query')
        category_slug = self.request.GET.get('category')

        if query:
            clean_query = query.strip()

            queryset = queryset.filter(
                Q(title__icontains=clean_query) |
                Q(author__name__icontains=clean_query)
            ).distinct()

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        #print("запит:", queryset.query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

#DetailView - інформація про одну конкретну книгу
class BookDetailView(DetailView):
    model = Book
    template_name = 'shop/book_detail.html'
    context_object_name = 'book'

#CreateView - створення нової книги
class BookCreateView(UserPassesTestMixin, CreateView):
    model = Book
    template_name = 'shop/book_form.html'
    fields = ['title', 'author', 'category', 'price', 'publisher_year', 'amount', 'available', 'publisher']
    success_url = reverse_lazy('shop:book_list')

    def test_func(self):
        return self.request.user.is_authenticated

#UpdateView - видалення книги
class BookUpdateView(UserPassesTestMixin, UpdateView):
    model = Book
    template_name = ('shop/book_form.html')
    fields = ['title', 'author', 'category', 'price', 'publisher_year', 'amount', 'available', 'publisher']
    success_url = reverse_lazy('shop:book_list')

    def test_func(self):
        return self.request.user.is_authenticated

#DeleteView - видалення книги
class BookDeleteView(UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'shop/book_confirm_delete.html'
    success_url = reverse_lazy('shop:book_list')

    def test_func(self):
        return self.request.user.is_authenticated

def custom_404_view(request, exception):
    return render(request, 'shop/error_404.html', status=404)