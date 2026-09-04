from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.conf import settings
from .models import Book, Category

@receiver(post_save, sender=Book)
@receiver(post_delete, sender=Book)
def invalidate_book_cache(sender, instance, **kwargs):
    cache.delete(f'book_detail_{instance.id}')

    for lang_code in settings.LANGUAGES:
        template_cache_key = make_template_fragment_key('book_card_info',[instance.id, lang_code])
        cache.delete(template_cache_key)

@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def invalidate_category_cache(sender, instance, **kwargs):
    cache.clear()