import requests
from django.conf import settings

def check_stock(book_id):
    try:
        print(f"DEBUG: Направляємо запит на склад для ID: {book_id}")
        token = settings.WAREHOUSE_API_TOKEN
        headers = {'Authorization': f'Bearer {token}'}

        url = f'{settings.WAREHOUSE_API_URL}{book_id}'

        response = requests.get(url, headers=headers, timeout=5)
        print(f"DEBUG: Статус: {response.status_code}, Відповідь: {response.text}")

        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException as e:
        print(f"DEBUG: Помилка з'єднання зі складом: {e}")
        return None