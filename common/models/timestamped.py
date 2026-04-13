from django.db import models

class TimestampedModel(models.Model):
    """ Base model with timestamp fields """
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True 