from django.urls import path

from order import views
from order.views import CartView, add_to_cart, remove_from_cart

app_name = 'order'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart_detail'),
    # Додали слеш в кінці та прибрали слово "views."
    path('add/<int:book_id>/', add_to_cart, name='add_to_cart'),

    path('remove/<int:book_id>', remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.create_checkout_session, name='create_checkout_session'),
    path('success/',views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
]