from apps.restaurants.models import Restaurant

class RestaurantSelector:

    @staticmethod
    def get_restaurant_queryset():
        return (
            Restaurant.objects.filter(is_deleted=False)
        )
    
    @staticmethod
    def get_popular_restaurants():
        return (
            Restaurant.objects.filter(is_deleted=False,is_open=True).order_by('-average_rating')
        )
    
    @staticmethod
    def get_own_restaurant_queryset(*, user):
        return (
            Restaurant.objects.filter(owner=user, is_deleted=False)
        )
    
    @staticmethod
    def get_none_restaurant():
        """no address for unauthenticated users"""
        return Restaurant.objects.none()