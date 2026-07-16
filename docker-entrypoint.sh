#!/bin/bash

echo "🚀 Запуск автоматичних міграцій..."
python manage.py migrate --noinput

echo "📁 Збір статичних файлів..."
python manage.py collectstatic --noinput

echo "✅ Сервер готовий!"
# Ця команда передає управління назад до docker-compose (наприклад, для runserver)
exec "$@"