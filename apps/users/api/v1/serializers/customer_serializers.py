from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from apps.users.models import CustomerProfile
from common.utils.validators import (
    validate_image_format,
    validate_image_size_5mb
)
from .address_serializers import AddressSerializer


class CustomerProfileSerializer(serializers.ModelSerializer):
    """ Customer profile serializer with required fields """
    avatar = serializers.ImageField(validators=[validate_image_format, validate_image_size_5mb], required=False)  
    default_address = serializers.SerializerMethodField()

    class Meta:
        model = CustomerProfile
        fields = ['id','user', 'avatar', 'total_orders', 'loyalty_points','default_address']
        read_only_fields = ['id','user', 'total_orders', 'loyalty_points']  

    @extend_schema_field(OpenApiTypes.STR)
    def get_default_address(self, obj):
         # print(obj)
        address = obj.default_address      
        if address:
            return AddressSerializer(address).data
        return None
