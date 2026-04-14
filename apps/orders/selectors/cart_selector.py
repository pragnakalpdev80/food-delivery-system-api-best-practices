from apps.orders.models import Cart, CartItem


class CartSelector:

    @staticmethod
    def get_cart_queryset(*, user):
        """Queryset of the customer's own profile — scoped to one user."""
        return (
            Cart.objects.prefetch_related('cart_items', 'cart_items__menu_item')
            .filter(customer=user)
        )

    @staticmethod
    def get_none_cart():
        """no address for unauthenticated users"""
        return Cart.objects.none()

    @staticmethod
    def get_cartitem_queryset(*, user):
        """Queryset of the customer's own profile — scoped to one user."""
        return (
            CartItem.objects.select_related('menu_item')
            .filter(cart__customer=user)
        )

    @staticmethod
    def get_none_cartitem():
        """no address for unauthenticated users"""
        return CartItem.objects.none()