# 📚 Django Book Shop Project

[![Render Deploy](https://img.shields.io/badge/Render-Live-46E3B7?style=flat-square&logo=render&logoColor=white)](https://book-shop-web.onrender.com)
![Coverage](./coverage.svg)

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

Для запуску тестів:
#bash
docker-compose exec web pytest
docker-compose exec web pytest --cov=. --cov-report=term-missing

AI Usage
Штучний інтелект (Gemini) був використаний як асистент у процесі розробки:
C
ode Review: Проведено аналіз функцій async_book_list, BookCreateView та create_checkout_session. ШІ виявив вразливості в авторизації (відсутність перевірки is_staff), логічні помилки в передачі лінивих QuerySet у контекст та ризики підміни ціни в кошику перед оплатою Stripe. Рекомендації були успішно впроваджені (деталі у файлі AI_REVIEW.md).

Генерація Тестів: Згенеровано базові unit-тести для моделей Publisher, Author та DeliveryAddress з використанням factory-boy.

Документація: Згенеровано Google-style docstrings для основних views та структуру цього README.