import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class WarehouseClient:
    """Клієнт для взаємодії з мікросервісом Warehouse"""

    def __init__(self):
        self.base_url = getattr(settings, 'WAREHOUSE_API_URL', 'http://warehouse:8000/api/')
        self.token = None

    def _get_token(self):
        """Отримує JWT-токен від мікросервісу складу"""
        try:
            response = requests.post(f"{self.base_url}token/", json={
                "username": settings.WAREHOUSE_USER,
                "password": settings.WAREHOUSE_PASSWORD
            }, timeout=5)

            if response.status_code == 200:
                self.token = response.json().get('access')
                return self.token
            else:
                logger.error(f"Помилка авторизації на складі: {response.text}")
        except requests.exceptions.RequestException as e:
            logger.critical(f"Не вдалося підключитися до сервісу токенів складу: {e}")
        return None

    def get_stock(self, book_id):
        """Отримує актуальний залишок товару зі складу"""
        token = self._get_token()
        if not token:
            return None

        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.get(f"{self.base_url}inventory/{book_id}/", headers=headers, timeout=5)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                logger.warning(f"Товар з ID {book_id} не знайдено на складі.")
                return None
            else:
                logger.error(f"Помилка отримання залишків: статус {response.status_code}")

        except requests.exceptions.Timeout:
            logger.error("Склад не відповів вчасно (Timeout).")
        except requests.exceptions.RequestException as e:
            logger.critical(f"Мережева помилка при зверненні до складу: {e}")

        return None