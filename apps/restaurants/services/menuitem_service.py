from django.db import transaction
from django.core.cache import cache

class MenuItemService:
    
    @staticmethod
    @transaction.atomic
    def soft_delete_menu(*, item, **data):
        item.is_deleted=True
        item.save(update_fields=['is_deleted','updated_at'])
    
    def clear_cache():
        cache.delete_many(['list_restaurant','retrieve_restaurant','restaurant_menu'])
