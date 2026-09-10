# 📚 Django Book Shop Project

[![Build Status](https://github.com/YuliiaRoz/Book_shop/actions/workflows/django.yml/badge.svg)](https://github.com/YuliiaRoz/Book_shop/actions)
[![Coverage Status](https://codecov.io/gh/YuliiaRoz/Book_shop/branch/main/graph/badge.svg)](https://codecov.io/gh/YuliiaRoz/Book_shop)

Сучасний веб-додаток для продажу книг, розроблений на Django. Проєкт фокусується на високій продуктивності, безпеці та сучасному тестуванні.

## 🚀 Основний функціонал
* **Асинхронність:** Використання `async views` та асинхронних запитів до БД (через `sync_to_async` та асинхронні ітератори) для списку книг і деталей.
* **Інтернаціоналізація:** Підтримка двох мов (Українська та Англійська) через `.po`/`.mo` словники.
* **Stripe Інтеграція:** Безпечні платежі з перевіркою актуальності цін на бекенді.
* **Повноцінний кошик:** Додавання, видалення та зміна кількості товарів через сесії.
* **Авторизація та Дозволи:** Тільки адміністратори (Staff) можуть створювати, редагувати або видаляти книги.

## 🛠 Тестування
Проєкт має **90% покриття коду (Coverage)**. 
Тести написані за допомогою `pytest-django`, використовують `factory-boy` для фікстур та `unittest.mock.patch` для ізоляції зовнішніх API (Stripe, Email).

Для запуску тестів у Docker:
```bash
docker-compose exec web pytest
docker-compose exec web pytest --cov=. --cov-report=term-missing