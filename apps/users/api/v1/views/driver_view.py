import logging
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.users.api.v1.serializers.driver_serializers import DriverProfileSerializer
from apps.users.models import DriverProfile
from common.utils.permissions import IsDriver

logger = logging.getLogger(__name__)

@extend_schema_view(
    list=extend_schema(
        summary="Driver Profile",
        description="Driver profile",
        request= DriverProfileSerializer,
        responses={
            200:DriverProfileSerializer
        },
        tags=["Driver Profile"]),
    retrieve=extend_schema(
        summary="Driver Profile",
        description="Driver profile details",
        request= DriverProfileSerializer,
        responses={
            200:DriverProfileSerializer
        },
        tags=["Driver Profile"]),
    partial_update=extend_schema(
        summary="Update Driver Profile",
        description=" Update your profile details here",
        request= DriverProfileSerializer,
        responses={
            200:DriverProfileSerializer
        },
        tags=['Driver Profile']
    ),
    destroy=extend_schema(
        summary="Driver Profile",
        description = "We have added soft delete to delete driver profile",
        tags=['Driver Profile']
    ),
)
class DriverViewSet(viewsets.ModelViewSet):
    """ Driver ViewSet to manage driver's profile. """
    permission_classes = [IsAuthenticated, IsDriver]
    serializer_class = DriverProfileSerializer
    http_method_names = ['get','patch','delete']

    def get_queryset(self):
        """ Queryset to get drivers can only access own profile. """
        if not self.request.user.is_authenticated:
            return DriverProfile.objects.none()
        return DriverProfile.objects.select_related('user').filter(user=self.request.user,is_deleted=False)

    def perform_destroy(self, instance):
        """ Method to soft delete the driver profile. """
        instance.is_deleted = True
        instance.save()