from django.db import transaction

class ReviewService:

    @staticmethod
    @transaction.atomic
    def create(*, customer_profile, serializer, **data):
        serializer.save(customer=customer_profile)
