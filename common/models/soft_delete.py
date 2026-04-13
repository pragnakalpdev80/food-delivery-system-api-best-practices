from django.db import models

class SoftDeleteModel(models.Model):
    """ Soft Delete Model """
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True 
