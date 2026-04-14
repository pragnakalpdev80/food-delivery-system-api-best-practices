import logging
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from apps.orders.models import Cart
from apps.orders.api.v1.serializers.cart_serializers import CartSerializer
from apps.orders.selectors.cart_selector import CartSelector
from apps.orders.services.cart_service import CartService
from common.utils.permissions import IsCustomer

logger = logging.getLogger(__name__)

@extend_schema_view(
    list=extend_schema(
        summary="Cart",
        description="Cart",
        request=CartSerializer,
        responses={200:CartSerializer},
        tags=["Cart"]
    ),
    retrieve=extend_schema(
        summary="Cart Details",
        description="Cart Details",
        request=CartSerializer,
        responses={200:CartSerializer},
        tags=["Cart"]
    ),
    destroy=extend_schema(
        summary="This method is not allowed",
        description = "Customer cannot delete cart.",
        responses={
            405:{}
        },
        tags=['Cart']
    ),
    clear=extend_schema(
        summary="Clear the Cart",
        description = "Remove items from the cart.",
        responses={
            204:{}
        },
        tags=['Cart']
    ),
)
class CartViewSet(viewsets.ModelViewSet):
    """ Cart ViewSet to manage the cart of customers. """
    permission_classes = [IsAuthenticated, IsCustomer]
    serializer_class = CartSerializer
    http_method_names = ['get','delete']

    def get_queryset(self):
        """
        Customers can only access their own cart only.
        """
        if not self.request.user.is_authenticated:
            return CartSelector.get_none_cart()
        return CartSelector.get_cart_queryset(user=self.request.user.customer_profile)

    @action(detail=False, methods=['delete'], url_path='clear')
    def clear(self, request):
        """
        Method to remove all cart items from the cart.
        """
        try:
            cart = request.user.customer_profile.cart
            CartService.clear_cart(cart=cart)
        except Cart.DoesNotExist:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        """ Cart creation endpoint is bloacked beacause when a customer will register then customer's cart will be created automatically and every customer can have only one cart."""
        return Response({'error':'User can only have one cart'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
