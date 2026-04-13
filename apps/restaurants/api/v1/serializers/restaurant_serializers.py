from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from apps.restaurants.models import Restaurant
from common.utils.validators import (
    validate_image_format,
    validate_image_size_5mb,
    validate_image_size_10mb,
    validate_amount
)
from .menuitem_serializers import MenuItemSerializer
from apps.orders.api.v1.serializers.review_serializers import ReviewSerializer

class RestaurantSerializer(serializers.ModelSerializer):
    """ Restaurant serializer with required fields """
    logo = serializers.ImageField(validators=[validate_image_format, validate_image_size_5mb], required=False)    
    banner = serializers.ImageField(validators=[validate_image_format, validate_image_size_10mb], required=False)  
    delivery_fee = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[validate_amount])
    minimum_order = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[validate_amount])

    class Meta:
        model = Restaurant
        fields = ['id', 'owner', 'name', 'description', 'cuisine_type', 'address',   
                  'phone_no', 'email', 'logo', 'banner', 'opening_time',
                  'closing_time', 'is_open', 'delivery_fee', 'minimum_order',
                  'average_rating', 'total_reviews']
        read_only_fields = ['average_rating', 'total_reviews', 'owner']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        return Restaurant.objects.create(**validated_data)


class RestaurantDetailSerializer(serializers.ModelSerializer):
    """ Restaurant serializer with menu items of restaurants """
    menu_items = serializers.SerializerMethodField()   
    # reviews = serializers.SerializerMethodField()        
    is_open_now = serializers.SerializerMethodField()            

    class Meta:
        model = Restaurant
        fields = ['id', 'owner', 'name', 'description', 'cuisine_type', 'address',
                  'phone_no', 'email', 'logo', 'banner', 'opening_time',
                  'closing_time', 'is_open', 'is_open_now', 'delivery_fee', 'minimum_order',
                  'average_rating', 'total_reviews', 'menu_items']
        read_only_fields = ['average_rating', 'total_reviews', 'owner']

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_open_now(self, obj):
        """ method to check restaurant is open or not """
         # print(obj)
        return obj.is_currently_open()
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_menu_items(self, obj):
        """ method to get menu items of restaurant """
        items = obj.menu_items.filter(is_available=True)
        return MenuItemSerializer(items, many=True).data

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_reviews(self, obj):
        """ method to get reviews of restaurant """
        reviews = obj.reviews.all().order_by('-created_at')
        return ReviewSerializer(reviews, many=True).data
