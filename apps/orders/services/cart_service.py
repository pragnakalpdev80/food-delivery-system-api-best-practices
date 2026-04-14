from django.db import transaction


class CartService:

    @staticmethod
    @transaction.atomic
    def clear_cart(*, cart, **data):
        cart.cart_items.all().delete()
        cart.restaurant = None
        cart.save(update_fields=['restaurant', 'updated_at'])
    

