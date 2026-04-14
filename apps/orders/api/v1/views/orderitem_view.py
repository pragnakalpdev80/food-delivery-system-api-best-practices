import logging
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from apps.orders.api.v1.serializers.orderitem_serializers import OrderItemSerializer
from common.utils.permissions import IsOrderCustomer
from apps.orders.selectors.order_selector import OrderSelector

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        summary="Order Item",
        description="Order Items",
        request=OrderItemSerializer,
        responses={
            200:{OrderItemSerializer}
        },
        tags=["Order Item"]
    ),
    retrieve=extend_schema(
        summary="Order Item",
        description="Order Item details",
        request=OrderItemSerializer,
        responses={
            200:{OrderItemSerializer}
        },
        tags=["Order Item"]
    ),
)
class OrderItemViewSet(viewsets.ModelViewSet):
    """ Order items ViewSet to see the order items of customers. """
    permission_classes = [IsAuthenticated,IsOrderCustomer]
    serializer_class = OrderItemSerializer
    http_method_names = ['get']

    def get_queryset(self):
        """
        Customers can see thier own order's items only.
        Restaurant owners can see restaurants order's items only.
        delivery drivers can see assigned order's items only.
        """
        user = self.request.user
        if not self.request.user.is_authenticated:
            return OrderSelector.get_none_orderitem()
        return OrderSelector.get_order_items_for_user(user=user)

    def retrieve(self, request, *args, **kwargs):
        """ Override retrieve to enforce object-level permission on order items. """
        instance = self.get_object()
        user = request.user
        is_owner = (
            (user.user_type == 'customer' and instance.order.customer.user == user)
            or (user.user_type == 'restaurant_owner'
                and instance.order.restaurant.owner == user)
            or (user.user_type == 'delivery_driver'
                and instance.order.driver
                and instance.order.driver.user == user)
        )
        if not is_owner:
            return Response(
                {'detail': 'You do not have permission to view this order item.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return Response({'error':'Please order via Cart'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
    def partial_update(self, request, *args, **kwargs):
        """
        User cannot update the order items.
        """
        return Response({'error':'You cannot update order items'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
