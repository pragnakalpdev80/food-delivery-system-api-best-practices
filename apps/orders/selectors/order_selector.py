from apps.orders.models import Order, OrderItem


class OrderSelector:

    @staticmethod
    def get_order_queryset(*, user):
        """Queryset of the customer's own profile — scoped to one user."""
        
        qs = Order.objects.select_related('customer', 'restaurant', 'driver').prefetch_related('menu_item')
        
        if user.user_type == 'customer':
            return qs.filter(customer__user=user)
        elif user.user_type == 'restaurant_owner':
            return qs.filter(restaurant__owner=user)
        elif user.user_type == 'delivery_driver':
            return qs.filter(driver__user=user)
    
    @staticmethod
    def get_none_orderitem():
        """no address for unauthenticated users"""
        return OrderItem.objects.none()

    @staticmethod
    def get_order_items_for_user(*, user):
        """
        OrderItem queryset scoped by user type.
        """
        if user.user_type == 'customer':
            return OrderItem.objects.filter(order__customer__user=user)
        elif user.user_type == 'restaurant_owner':
            return OrderItem.objects.filter(order__restaurant__owner=user)
        elif user.user_type == 'delivery_driver':
            return OrderItem.objects.filter(order__driver__user=user)
    
    @staticmethod
    def get_none_order():
        """no address for unauthenticated users"""
        return Order.objects.none()
    
    @staticmethod
    def get_order(id):
        return Order.objects.filter(id=id).first()
