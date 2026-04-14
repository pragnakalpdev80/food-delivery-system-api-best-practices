import logging
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.orders.api.v1.serializers.cartitem_serializers import CartItemSerializer
from apps.orders.selectors.cart_selector import CartSelector
from common.utils.permissions import IsCustomer

logger = logging.getLogger(__name__)

@extend_schema_view(
    create=extend_schema(
        summary="Cart Item",
        description = "Cart Item creation",
        request= CartItemSerializer,
        responses={
            201:CartItemSerializer
        },
        tags=['Cart Item']
    ),
    list=extend_schema(
        summary="Cart Item",
        description="Cart Items",
        request= CartItemSerializer,
        responses={
            200:CartItemSerializer
        },
        tags=["Cart Item"]
    ),
    retrieve=extend_schema(
        summary="Cart Item",
        description="Cart Item details",
        request= CartItemSerializer,
        responses={
            200:CartItemSerializer
        },
        tags=["Cart Item"]
    ),
    partial_update=extend_schema(
        summary="Update Cart Item",
        description=" Update your Cart Items here.",
        request= CartItemSerializer,
        responses={
            200:CartItemSerializer
        },
        tags=['Cart Item']
    ),
    destroy=extend_schema(
        summary="Cart Item",
        description = "Remove item from the cart.",
        responses={
            204:{}
        },
        tags=['Cart Item']
    ),
)
class CartItemViewSet(viewsets.ModelViewSet):
    """ Cart ViewSet to manage the cart of customers. """
    permission_classes = [IsAuthenticated, IsCustomer]
    serializer_class = CartItemSerializer
    http_method_names = ['get', 'post', 'patch','delete']

    def get_queryset(self):
        """ customers can only acccess their own cart items only. """
        if not self.request.user.is_authenticated:
            return CartSelector.get_none_cartitem()
        return CartSelector.get_cartitem_queryset(user=self.request.user.customer_profile)