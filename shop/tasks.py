import time
import requests
import logging
from celery import shared_task
from django.core.management import call_command
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task
def send_order_email(user_email, order_id):
    time.sleep(2)
    return f"Email sent to {user_email} for order #{order_id}"

@shared_task
def clear_sessions():
    call_command('clear_sessions')
    return "Expired sessions cleared successfully"

@shared_task
def generate_reports():
    return "Daily reports generated"

@shared_task
def sync_book_with_warehouse(self, sku, name):
    token_url = f"{settings.WAREHOUSE_API_URL}/token/"
    sync_url = f"{settings.WAREHOUSE_API_URL}/inventory/sync-product"

    try:
        # отримуємо JWT токен
        token_response = requests.post(token_url, json={
            "username": settings.WAREHOUSE_USER,
            "password": settings.WAREHOUSE_PASSWORD
        }, timeout=5)

        token_response.raise_for_status()
        access_token = token_response.json().get('access')

        # відправляємо дані про товар
        headers = {'Authorization': f'Bearer {access_token}'}
        payload = {
            "sku": str(sku),
            "name": name
        }

        sync_response = requests.post(sync_url, json=payload, headers=headers, timeout=5)
        sync_response.raise_for_status()

        logger.info(f"Успішно синхронізовано товар {sku} зі Складом.")
        return sync_response.json()

    except requests.RequestException as e:
        logger.error(f"Помилка синхронізації зі Складом для товару {sku}: {e}")

        raise self.retry(exc=e, countdown=60)