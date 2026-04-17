import logging
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.orders.api.v1.serializers.order_serializers import OrderCreateSerializer,OrderSerializer, OrderDetailSerializer
from apps.orders.selectors.order_selector import OrderSelector
from common.utils.permissions import IsRestaurantOwner, IsRestaurantOwnerOrDriver, IsOwnerOrReadOnly, IsCustomer
from common.api.filters import OrderFilter
from common.api.throttles import OrderCreateThrottle, CustomerRateThrottle
from common.api.pagination import OrderCursorPagination
from apps.orders.services.order_service import OrderService

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        summary="Order",
        description="Order",
        request=OrderSerializer,
        responses={
            200:OrderSerializer
        },
        tags=["Order"]
    ),
    retrieve=extend_schema(
        summary="Order",
        description="Order details",
        request=OrderDetailSerializer,
        responses={
            200:OrderDetailSerializer
        },
        tags=["Order"]
    ),
    update_status=extend_schema(
        summary="Order Status Update",
        description = "Order Status Update.",
        request=OrderSerializer,
        responses={
            200:{}
        },
        tags=['Order']
    ),
    assign_driver=extend_schema(
        summary="Driver Assign to Order",
        description = "Assign the driver to the order.",
        request=OrderSerializer,
        responses={
            200:{}
        },
        tags=['Order']
    ),
    cancel=extend_schema(
        summary="Cancel Order",
        description = "Customer can cancel the order if it is not preapared.",
        request=OrderSerializer,
        responses={
            200:{}
        },
        tags=['Order']
    ),
    place=extend_schema(
        summary="Place Order",
        description = "Customers can place orders from here.",
        request=OrderCreateSerializer,
        responses={
            200:{OrderCreateSerializer}
        },
        tags=['Order']
    ),
    create=extend_schema(
        summary="Create Order",
        description = "Customer can order from cart only",
        responses={
            405:{}
        },
        tags=['Order']
    ),
)
class OrderViewSet(viewsets.ModelViewSet):
    """ Order ViewSet to manage the order of customers. """
    permission_classes = [IsAuthenticated]
    pagination_class =OrderCursorPagination
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['order_number']
    ordering_fields = ['total_amount',]
    ordering = ['-created_at']
    http_method_names = ['get', 'post']

    def retrieve(self, request, *args, **kwargs):
        """ Only order customer, restaurant and drivers can access own orders. """
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        OrderService.retrieve(order_id=instance.id)
        return Response(serializer.data)

    def get_serializer_class(self):
        """ Different serializers for different method as per required fields. """
        if self.action in ['retrieve']:
            return OrderDetailSerializer
        if self.action == 'place':
            return OrderCreateSerializer
        return OrderSerializer
    
    def get_permissions(self):
        """
        Permissions for different actions.
        """
        if self.action in ['place', 'cancel']:
            return [IsAuthenticated(), IsCustomer()]
        if self.action in ['assign-driver', 'cancel']:
            return [IsAuthenticated(), IsRestaurantOwner(), IsOwnerOrReadOnly()]
        if self.action in ['update_status']:
            return [IsAuthenticated(), IsRestaurantOwnerOrDriver()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Customers can see thier own orders.
        Restaurant owners can see restaurants orders only.
        delivery drivers can see assigned orders only.
        """
        user = self.request.user
        if not self.request.user.is_authenticated:
            return OrderSelector.get_none_order()
        OrderSelector.get_order_queryset(user=user)
    
   
    @action(detail=False, methods=['post'], url_path='place', throttle_classes=[OrderCreateThrottle])
    def place(self, request, *args, **kwargs):
        """
        cart to place the order
        """
        if request.user.user_type != 'customer':
            return Response({'message': 'Only customers can place orders.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderDetailSerializer(order, context={'request': request}).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request,  *args, **kwargs):
        """
        Custom method to cancel the order.
        """
        order = self.get_object()
        user_type = request.user.user_type
        OrderService.cancel(order=order, user_type=user_type)
        
        return Response({'success': 'Order cancelled successfully.'},status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='update-status')
    def update_status(self, request,  *args, **kwargs):
        """
        Custom method to update the order status
        """
        if request.user.user_type == 'customer':
            return Response({'message': 'Only Restaurants and Driver can update order status.'}, status=status.HTTP_403_FORBIDDEN)

        user_type = request.user.user_type
        order = self.get_object()
        self.check_object_permissions(request, order)
        new_status = request.data.get('status')
        if not new_status:
            return Response(
                {'error': 'status field is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        OrderService.update_status(order=order, user_type=user_type, new_status=new_status)
        
        return Response({'success': f'Order status updated to {new_status}.'},status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='assign-driver')
    def assign_driver(self, request,  *args, **kwargs):
        """
        Custom method to assign the driver to order.
        """
        order = self.get_object()
        self.check_object_permissions(request, order)
        OrderService.assign_driver(order=order)
        return Response({'detail': f'Driver assigned successfully.'},status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Create method is blocked because we are allowing to order from the cart only.
        """
        return Response({'error':'You cannot create orders directly use place method to create orders'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
