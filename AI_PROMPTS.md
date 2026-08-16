# Список промптів, використаних у проєкті

## 1. Code Review (Виявлення вразливостей)
> "Act as a Senior Django Security Expert. Please review the following Django views: `BookCreateView`, `async_book_list`, and `create_checkout_session`. Look for security vulnerabilities, data integrity issues, and performance bottlenecks. Suggest improvements and provide the refactored code."

> "Which of these recommendations should I provide in my project??"

Here's a prioritized punch list — split into what's mandatory before this touches production and what can wait.

🔴 Ship these before anything else (security/data-integrity bugs)
BookCreateView — fix test_func. This is the most serious issue in the whole review: any logged-in user can currently create books. Change to is_staff (or a proper permission check). Do this first, today.
create_checkout_session — add @login_required. Right now an anonymous user hitting this view breaks or creates broken data tied to no one.
create_checkout_session — stop trusting item['price'] from the cart. Recompute price from book.price in the DB at checkout time. This is a real "pay whatever you want" vulnerability if the cart price can ever go stale or be tampered with.
create_checkout_session — add @require_http_methods(['GET', 'POST']) / guard against GET creating a Stripe session. Prevents accidental/duplicate Stripe API calls and orphaned DeliveryAddress rows.
async_book_list — fix the context bug (books_list computed but never used; page_obj.object_list passed instead). This is likely actively broken or crashing depending on your Django version — verify in your actual app.