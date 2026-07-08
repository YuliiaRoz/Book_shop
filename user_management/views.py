import logging
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

logger = logging.getLogger(__name__)
# Create your views here.
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user_management/register.html'
    success_url = reverse_lazy('shop:book_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)

        logger.info(f"User {self.object.username} registered successfully!")

        return response

class CustomLoginView(LoginView):
    template_name = 'user_management/login.html'

    def get_success_url(self):
        return reverse_lazy('shop:book_list')