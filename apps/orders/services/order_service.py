from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.users.selectors.user_selector import UserSelector
from rest_framework.response import Response
from apps.users.models import DriverProfile
from rest_framework import status
from datetime import datetime

class OrderService:

    @staticmethod
    @transaction.atomic
    def cancel(*, order,user_type, **data):
        if user_type == 'delivery_driver':
            return Response({'error': 'Driver cannot cancel the order.'}, status=status.HTTP_400_BAD_REQUEST)
        if not order.can_cancel():
            return Response({'error': 'This order cannot be cancelled.'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = 'cancelled'
        order.save(update_fields=['status', 'updated_at'])
        if order.driver:
            driver = DriverProfile.objects.filter(id=order.driver.id).first()
            driver.update_availability(True)
            driver.save(update_fields=['updated_at','is_available'])
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"restaurant_{order.restaurant.id}",
            {
                "type": "order_status_update",
                "order_id": str(order.order_number),
                "status":order.status,
                "message": "Order cancelled!"
            }
        )

        async_to_sync(channel_layer.group_send)(
            f"order_{order.order_number}",
            {
                "type": "order_status_update",
                "order_id": str(order.order_number),
                "status":order.status,
                "message": "Order cancelled!"
            }
        )

        async_to_sync(channel_layer.group_send)(
            f"customer_{order.customer.id}",
            {
                "type": "order_status_update",
                "order_id": str(order.order_number),
                "status":order.status,
                "message": "Order cancelled!"
            }
        )

    @staticmethod
    @transaction.atomic
    def update_status(*,user_type,new_status,order, **data):
        if user_type == 'restaurant_owner':
            if new_status not in ['confirmed','preparing','ready']:
                return Response({'error': f'{new_status} status is not valid'},status=status.HTTP_400_BAD_REQUEST)
            
            elif order.status == 'pending':
                if new_status != 'confirmed':
                    return Response({'error': f'Please confirm the order first.'},status=status.HTTP_400_BAD_REQUEST)
                
            elif order.status == 'confirmed':
                if new_status != 'preparing':
                    return Response({'error': f'Please prepare the order first.'},status=status.HTTP_400_BAD_REQUEST)
                
            elif order.status == 'preparing':
                if new_status != 'ready':
                    return Response({'error': f'Please ready the order first.'},status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'error': f'You can not do more actions.'},status=status.HTTP_400_BAD_REQUEST)
            
        if user_type == 'delivery_driver':
            if new_status not in ['picked_up','delivered']:
                return Response({'error': f'{new_status} status is not valid'},status=status.HTTP_400_BAD_REQUEST)

            elif order.status == 'ready':
                if new_status != 'picked_up':
                    return Response({'error': f'Please pick up the order first.'},status=status.HTTP_400_BAD_REQUEST)
            
            elif order.status == 'picked_up':
                if new_status != 'delivered':
                    return Response({'error': f'Please deliver the order.'},status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'error': f'You can not do more actions.'},status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save(update_fields=['status', 'updated_at'])
        if order.status == 'delivered':
            order.actual_delivery_time = datetime.now()
            order.save(update_fields=['actual_delivery_time'])
            driver = DriverProfile.objects.filter(id=order.driver.id).first()
            driver.update_availability(True)
            driver.save(update_fields=['updated_at','is_available'])
        #web socket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"restaurant_{order.restaurant.id}",
            {
                "type": "order_status_update",
                "order_id": str(order.order_number),
                "status":order.status,
                "message": "Order status updated!"
            }
        )

        async_to_sync(channel_layer.group_send)(
            f"order_{order.order_number}",
            {
                "type": "order_status_update",
                "order_id": str(order.order_number),
                "status":order.status,
                "message": "Order status updated!"
            }
        )
        
        if order.driver:
            async_to_sync(channel_layer.group_send)(
                f"driver_{order.driver.id}",
                {
                    "type": "order_status_update_driver",
                    "order_id": str(order.order_number),
                    "status":order.status,
                    "message": "Order status updated!"
                }
            )

    @staticmethod
    @transaction.atomic
    def assign_driver(*, order, **data):
        try:
            driver = UserSelector.get_available_driver()
            if not driver:
                return Response({'detail': 'No available driver found.'}, status=status.HTTP_404_NOT_FOUND)
        except DriverProfile.DoesNotExist:
            return Response({'detail': 'Driver not found.'}, status=status.HTTP_404_NOT_FOUND)
        order.driver = driver
        driver.update_availability(False)
        driver.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
                f"driver_{order.driver.id}",
                {
                    "type": "order_status_update_driver",
                    "order_id": str(order.order_number),
                    "status":order.status,
                    "message": "Order status updated!"
                }
            )
        
        async_to_sync(channel_layer.group_send)(
            f"order_{order.order_number}",
            {
                "type": "order_status_update",
                "order_id": str(order.order_number),
                "status":order.status,
                "message": "Order status updated!"
            }
        )

        order.save(update_fields=['driver', 'updated_at'])
        