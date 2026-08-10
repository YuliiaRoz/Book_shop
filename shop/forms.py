from django import forms
from django.utils.translation import gettext_lazy as _

class SearchForm(forms.Form):
    query = forms.CharField(
        label = _('Що шукаємо?'),
        max_length=100,
        required = False,
        widget = forms.TextInput(attrs={'placehoder': _('Введіть назві або опис...')})
    )
