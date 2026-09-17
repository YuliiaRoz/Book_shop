import requests

WAREHOUSE_URL = 'http://192.168.0.102:8001/api/inventory/'

API_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg5ODAzMzQ0LCJpYXQiOjE3ODk2MzA1NDQsImp0aSI6Ijc2YTQ5ODA4M2I3NTRiMWM4Yjc0NDhlYzlhNDg5N2YwIiwidXNlcl9pZCI6IjEifQ.MkDfI5tDnPPweLfEMnhNHr0DqaY2xHqNbK431vjB4Xo'

def check_stock(book_id):
    try:
        print(f"DEBUG: Направляємо запит на склад для ID: {book_id}")
        headers = {'Authorization': f'Bearer {API_TOKEN}'}

        response = requests.get(f'{WAREHOUSE_URL}{book_id}', headers=headers, timeout=5)
        print(f"DEBUG: Статус: {response.status_code}, Відповідь: {response.text}")

        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException as e:
        print(f"DEBUG: Помилка з'єднання зі складом: {e}")
        return None