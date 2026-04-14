from apps.orders.models import Review


class ReviewSelector:

    @staticmethod
    def get_review_queryset(*, user):
        """Queryset of the customer's own profile — scoped to one user."""
        return (
            Review.objects.filter(customer__user=user)
        )

    @staticmethod
    def get_none_review():
        """no address for unauthenticated users"""
        return Review.objects.none()