from apps.restaurants.models import MenuItem

class MenuItemSelector:

    @staticmethod
    def get_menuitem_queryset(*, user):
        if user.user_type == 'restaurant_owner':
            return(
                MenuItem.objects.filter(restaurant__owner=user,is_deleted=False).select_related('restaurant')
            )
        return (
            MenuItem.objects.filter(is_available=True,is_deleted=False).select_related('restaurant')
        )

    @staticmethod
    def get_restaurant_menu(*, restaurant):
        return (
            MenuItem.objects.select_related('restaurant').filter(restaurant=restaurant, is_available=True)
        )
    
    @staticmethod
    def get_none_menu():
        """no address for unauthenticated users"""
        return  MenuItem.objects.none()
    
    def get_menuitems_of_restaurants(*, restaurant):
        return MenuItem.objects.filter(restaurant=restaurant,is_deleted=False)