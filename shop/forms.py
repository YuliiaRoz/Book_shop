from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
        label = 'Що шукаємо?',
        max_length=100,
        required = False,
        widget = forms.TextInput(attrs={'placehoder': 'Введіть назві або опис...'})
    )
