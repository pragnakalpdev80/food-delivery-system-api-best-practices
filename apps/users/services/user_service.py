from django.db import transaction

class UserService:
    
    @staticmethod
    @transaction.atomic
    def soft_delete(*, user, **data):
        user.is_deleted=True
        user.save(update_fields=['is_deleted','updated_at'])
