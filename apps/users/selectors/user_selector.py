from apps.users.models import User, CustomerProfile, DriverProfile, Address


class UserSelector:

    @staticmethod
    def get_customer_profile(*, user):
        """Return the customer profile for a given user (not deleted)."""
        return (
            CustomerProfile.objects.select_related('user')
            .filter(user=user, is_deleted=False).first()
        )

    @staticmethod
    def get_customer_profile_queryset(*, user):
        """Queryset of the customer's own profile — scoped to one user."""
        return (
            CustomerProfile.objects
            .select_related('user')
            .filter(user=user, is_deleted=False)
        )

    @staticmethod
    def get_none_customer():
        """no address for unauthenticated users"""
        return CustomerProfile.objects.none()

    @staticmethod
    def get_available_driver():
        """Return the driver profile for a given user (not deleted)."""
        return (
            DriverProfile.objects.filter(is_available=True).first()
        )

    @staticmethod
    def get_driver_profile_queryset(*, user):
        """Queryset of the driver's own profile — scoped to one user."""
        return (
            DriverProfile.objects
            .select_related('user')
            .filter(user=user, is_deleted=False)
        )
    
    @staticmethod
    def get_none_driver():
        """no address for unauthenticated users"""
        return DriverProfile.objects.none()

    @staticmethod
    def get_available_driver():
        """Return the first available driver for assignment."""
        return (
            DriverProfile.objects
            .select_related('user').filter(is_available=True, is_deleted=False).first()
        )

    @staticmethod
    def get_address_queryset(*, user):
        """All addresses of the given user."""
        return (
            Address.objects.select_related('user').filter(user=user, is_deleted=False)
        )

    @staticmethod
    def get_address(*, address_id, user):
        """default address of the User."""
        return (
            Address.objects.filter(id=address_id, user=user, is_deleted=False).first()
        )
    
    @staticmethod
    def get_none_address():
        """no address for unauthenticated users"""
        return Address.objects.none()