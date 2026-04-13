from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    User, 
    CustomerProfile, 
    DriverProfile,
)
from apps.orders.models import Cart

@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    """
    To Create Customer and Driver Profiles
    """
    if created:
        if instance.user_type == 'customer':
            CustomerProfile.objects.create(user=instance)
        elif instance.user_type == 'delivery_driver':
            DriverProfile.objects.create(user=instance) 

@receiver(post_save, sender=CustomerProfile)
def create_cart_on_customer_creation(sender, instance, created, **kwargs):
    """
    To create cart of customer automatically
    """
    if created:
        Cart.objects.create(customer=instance)
