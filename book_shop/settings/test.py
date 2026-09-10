import os
from .base import *  # або імпорт з production, залежно від того, що ви використовували

# Встановлюємо значення за замовчуванням для тестів, якщо вони не передані ззовні
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

# Перевизначаємо кеш для тестів (щоб не чіпати реальний Redis)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}