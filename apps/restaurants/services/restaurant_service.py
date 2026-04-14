from django.db import transaction
from apps.restaurants.selectors.menuitem_selector import MenuItemSelector
from django.core.cache import cache

class RestaurantService:
    
    @staticmethod
    @transaction.atomic
    def soft_delete_restaurant(*, restaurant, **data):
        restaurant.is_deleted=True
        restaurant.save(update_fields=['is_deleted','updated_at'])
        menu_items = MenuItemSelector.get_menuitems_of_restaurants(restaurant=restaurant)
        for menu_item in menu_items:
            menu_item.is_deleted = True
            menu_item.save()

    def clear_restaurant_cache():
        cache.delete_many(['list_restaurant','retrieve_restaurant','restaurant_menu'])
