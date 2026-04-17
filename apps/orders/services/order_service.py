from django.db import transaction
from apps.users.selectors.user_selector import UserSelector
from rest_framework.response import Response
from apps.users.models import DriverProfile
from rest_framework import status
from datetime import datetime
from apps.orders.tasks import broadcast_order_update, broadcast_new_order
from common.exceptions.domain import (
    OrderCannotBeCancelled,
    DriverCannotCancelOrder,
    NoAvailableDriver,
    InvalidOrderStatus,
    OrderNotFound,
    NotValidAction,
    CanNotPerformAction
)
from apps.orders.selectors.order_selector import OrderSelector


class OrderService:

    @staticmethod
    @transaction.atomic
    def cancel(*, order,user_type, **data):
        if user_type == 'delivery_driver':
            return DriverCannotCancelOrder()
        if not order.can_cancel():
            return OrderCannotBeCancelled()
        order.status = 'cancelled'
        order.save(update_fields=['status', 'updated_at'])
        if order.driver:
            driver = DriverProfile.objects.filter(id=order.driver.id).first()
            driver.update_availability(True)
            driver.save(update_fields=['updated_at','is_available'])
            broadcast_order_update.delay(f"driver_{order.driver.id}",
                               "order_status_update_driver",str(order.order_number),
                               order.status,"Order cancelled!")
        
        broadcast_order_update.delay(f"customer_{order.customer.id}",
                               "order_status_update_customer",str(order.order_number),
                               order.status,"Order cancelled!")
        broadcast_order_update.delay(f"restaurant_{order.restaurant.id}",
                               "order_status_update_restaurant",str(order.order_number),
                               order.status,"Order cancelled!")

        broadcast_order_update.delay(f"order_{order.order_number}",
                                    "order_status_update",str(order.order_number),
                                    order.status,"Order cancelled!")

    @staticmethod
    @transaction.atomic
    def update_status(*,user_type,new_status,order, **data):
        if user_type == 'restaurant_owner':
            if new_status not in ['confirmed','preparing','ready']:
                raise NotValidAction(user_type, new_status)
            
            elif order.status == 'pending':
                if new_status != 'confirmed':
                    raise InvalidOrderStatus(order.status,new_status)
                
            elif order.status == 'confirmed':
                if new_status != 'preparing':
                    raise InvalidOrderStatus(order.status,new_status)
                
            elif order.status == 'preparing':
                if new_status != 'ready':
                    raise InvalidOrderStatus(order.status,new_status)

            else:
                raise CanNotPerformAction()
            
        if user_type == 'delivery_driver':
            if new_status not in ['picked_up','delivered']:
                raise NotValidAction(user_type, new_status)

            elif order.status == 'ready':
                if new_status != 'picked_up':
                    raise InvalidOrderStatus(order.status,new_status)
            
            elif order.status == 'picked_up':
                if new_status != 'delivered':
                    raise InvalidOrderStatus(order.status,new_status)

            else:
                raise CanNotPerformAction()
            
        order.status = new_status
        order.save(update_fields=['status', 'updated_at'])
        if order.status == 'delivered':
            order.actual_delivery_time = datetime.now()
            order.save(update_fields=['actual_delivery_time'])
            driver = DriverProfile.objects.filter(id=order.driver.id).first()
            driver.update_availability(True)
            driver.save(update_fields=['updated_at','is_available'])
                
        if order.driver:
                broadcast_order_update.delay(f"driver_{order.driver.id}",
                               "order_status_update_driver",str(order.order_number),
                               order.status,"Order status updated!")
        
        broadcast_order_update.delay(f"customer_{order.customer.id}",
                               "order_status_update_customer",str(order.order_number),
                               order.status,"Order status updated!")
        broadcast_order_update.delay(f"restaurant_{order.restaurant.id}",
                               "order_status_update_restaurant",str(order.order_number),
                               order.status,"Order status updated!")

        broadcast_order_update.delay(f"order_{order.order_number}",
                                    "order_status_update",str(order.order_number),
                                    order.status,"Order status updated!")


    @staticmethod
    @transaction.atomic
    def assign_driver(*, order, **data):
        try:
            driver = UserSelector.get_available_driver()
            if not driver:
                return Response({'detail': 'No available driver found.'}, status=status.HTTP_404_NOT_FOUND)
        except DriverProfile.DoesNotExist:
            raise NoAvailableDriver()
        order.driver = driver
        driver.update_availability(False)
        driver.save()
        broadcast_order_update.delay(f"driver_{order.driver.id}",
                               "order_status_update_driver",str(order.order_number),
                               order.status,"Order status updated!")
        
        broadcast_order_update.delay(f"customer_{order.customer.id}",
                               "order_status_update_customer",str(order.order_number),
                               order.status,"Order status updated!")
        broadcast_order_update.delay(f"restaurant_{order.restaurant.id}",
                               "order_status_update_restaurant",str(order.order_number),
                               order.status,"Order status updated!")

        broadcast_order_update.delay(f"order_{order.order_number}",
                                    "order_status_update",str(order.order_number),
                                    order.status,"Order status updated!")


        order.save(update_fields=['driver', 'updated_at'])
    
    @staticmethod
    @transaction.atomic
    def retrieve(*, order_id, **data):
        try:
            order=OrderSelector.get_order(order_id)
        except order.DoesNotExist:
            raise OrderNotFound()
