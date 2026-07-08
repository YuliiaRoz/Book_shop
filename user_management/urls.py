from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import RegisterView, CustomLoginView

app_name = 'user_management'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='shop:book_list'), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
]