import logging
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.users.api.v1.serializers.customer_serializers import CustomerProfileSerializer
from common.utils.permissions import IsCustomer
from apps.users.selectors.user_selector import UserSelector
from apps.users.services.user_service import UserService
from common.api.throttles import CustomerRateThrottle

logger = logging.getLogger(__name__)

@extend_schema_view(
    list=extend_schema(
        summary=" Customer Profile",
        description="Customer profile",
        request= CustomerProfileSerializer,
        responses={
            200:CustomerProfileSerializer
        },
        tags=["Customer Profile"]),
    retrieve=extend_schema(
        summary=" Customer Profile",
        description="Customer profile details",
        responses={
            200:CustomerProfileSerializer
        },
        tags=["Customer Profile"]),
    partial_update=extend_schema(
        summary="Update Customer Profile",
        description=" Update your profile details here",
        request=CustomerProfileSerializer,
        responses={
            200:CustomerProfileSerializer
        },
        tags=['Customer Profile']
    ),
    destroy=extend_schema(
        summary="Customer Profile",
        description = "We have added soft delete to delete customer profile",
        tags=['Customer Profile']
    ),
)
class CustomerViewSet(viewsets.ModelViewSet):
    """
    Customer Viewset to manage customer profile.
    """
    permission_classes = [IsAuthenticated,IsCustomer]
    serializer_class = CustomerProfileSerializer
    http_method_names = ['get', 'patch', 'delete']
    throttle_classes = CustomerRateThrottle

    def get_queryset(self):
        """ Queryset to get customer can only access own profile. """
        if not self.request.user.is_authenticated:
            return UserSelector.get_none_customer()
        return UserSelector.get_customer_profile_queryset(user=self.request.user)

    def perform_destroy(self, instance):
        """ Method to soft delete the customer. """
        UserService.soft_delete(user=instance)
