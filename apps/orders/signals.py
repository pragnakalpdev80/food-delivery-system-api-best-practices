from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    Order, 
    Review
)
from apps.restaurants.services.restaurant_service import RestaurantService
from apps.orders.tasks import broadcast_new_order

@receiver(post_save, sender=Review)
def update_rating_on_review_save(sender, instance, created, **kwargs):
    """
    To Update Average Rating
    """
    if created:
        if instance.restaurant:
            instance.restaurant.update_average_rating()
            RestaurantService.clear_restaurant_cache()
    
@receiver(post_save, sender=Order)
def order_notification_to_restaurant(sender, instance, created, **kwargs):
    if created:
        broadcast_new_order.delay(f"restaurant_{instance.restaurant.id}",
                               "new_order",str(instance.order_number),
                               "New Order Arrived")

@receiver(post_save, sender=Order)
def update_stats_on_delivery(sender, instance, created, **kwargs):
    if not created and instance.status == 'delivered':
        customer = instance.customer
        customer.total_orders += 1
        customer.loyalty_points += 1
        customer.save(update_fields=['total_orders', 'loyalty_points', 'updated_at'])
        
        if instance.driver:
            driver = instance.driver
            driver.total_deliveries += 1
            driver.is_available = True
            driver.save(update_fields=['total_deliveries', 'is_available', 'updated_at'])