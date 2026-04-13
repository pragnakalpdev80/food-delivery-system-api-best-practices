import logging
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.users.api.v1.serializers.address_serializers import AddressSerializer
from apps.users.models import Address
from common.utils.permissions import IsCustomer

logger = logging.getLogger(__name__)

@extend_schema_view(
    create=extend_schema(
        summary="Customer Address",
        description = "Customer Address creation",
        request= AddressSerializer,
        responses={
            201:AddressSerializer
        },
        tags=['Customer Address']
    ),
    list=extend_schema(
        summary="Customer Address",
        description="Customer Addresses",
        request= AddressSerializer,
        responses={
            200:AddressSerializer
        },
        tags=["Customer Address"]),
    retrieve=extend_schema(
        summary="Customer Address",
        description="Customer Address details",
        request= AddressSerializer,
        responses={
            200:AddressSerializer
        },
        tags=["Customer Address"]),
    partial_update=extend_schema(
        summary="Update Customer Address",
        description=" Update your Address details here",
        request= AddressSerializer,
        responses={
            200:AddressSerializer
        },
        tags=['Customer Address']
    ),
    destroy=extend_schema(
        summary="Soft deletion of customer address",
        description = "We have added soft delete to delete customer address",
        request= AddressSerializer,
        responses={
            204:{}
        },
        tags=['Customer Address']
    ),
)
class AddressViewSet(viewsets.ModelViewSet):
    """
    Customer Viewset to manage customer addresses.
    """
    permission_classes = [IsAuthenticated, IsCustomer]
    serializer_class = AddressSerializer
    http_method_names = ['get', 'post', 'patch','delete']

    def get_queryset(self):
        """ Only customers can manage own addresses only"""
        if not self.request.user.is_authenticated:
            return Address.objects.none()
        return Address.objects.select_related('user').filter(user = self.request.user,is_deleted=False)
    
    def perform_destroy(self, instance):
        """ Method to soft delete the address. """
        instance.is_deleted = True
        instance.save()
