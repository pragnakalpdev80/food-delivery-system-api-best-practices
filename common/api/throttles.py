from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class OrderCreateThrottle(UserRateThrottle):
    """
    This throttle will limit the rate of order creation till 20 attempts per hour.
    """
    scope = 'order_create'
    rate = '20/hour'

class ReviewCreateThrottle(UserRateThrottle):
    """
    This throttle will limit the rate of review creation till 10 attempts per hour.
    """
    scope = 'review_create'
    rate = '10/hour'

class LocationUpdateThrottle(UserRateThrottle):
    """
    This throttle will limit the rate of location updates till 500 attempts per hour.
    """
    scope = 'location_update'
    rate = '500/hour'

class LoginRateThrottle(AnonRateThrottle):
    """
    Login Endpoint Throttle
    """
    scope = 'login'


class RegistrationRateThrottle(AnonRateThrottle):
    """
    registration endpoint throttle
    """
    scope = 'registration'


class CustomerRateThrottle(UserRateThrottle):
    """ A customer can do 1000 requests per hour """
    scope = 'customer'
    rate = '1000/hour'


class RestaurantOwnerRateThrottle(UserRateThrottle):
    """ A restaurant owner can do 1000 requests per hour """

    scope = 'restaurant_owner'
    rate = '500/hour'


class DriverRateThrottle(UserRateThrottle):
    """ A driver can do 1000 requests per hour """
    scope = 'driver'
    rate = '500/hour'