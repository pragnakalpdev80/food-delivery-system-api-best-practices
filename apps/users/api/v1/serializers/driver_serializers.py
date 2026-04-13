from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from apps.users.models import DriverProfile
from common.utils.validators import (
    validate_image_format,
    validate_image_size_5mb
)

class DriverProfileSerializer(serializers.ModelSerializer):
    """ Driver profile serializer with required fields """
    avatar = serializers.ImageField(validators=[validate_image_format, validate_image_size_5mb], required=False)   
    delivery_stats = serializers.SerializerMethodField()

    class Meta:
        model = DriverProfile
        fields = ['id','user', 'avatar', 'vehicle_type', 'vehicle_number', 'delivery_stats',
                  'license_number', 'is_available',]
        read_only_fields = ['id','user', 'delivery_stats']  

    @extend_schema_field(OpenApiTypes.STR)
    def get_delivery_stats(self, obj):
        return obj.get_delivery_stats()