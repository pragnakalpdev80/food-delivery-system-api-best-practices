from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from apps.orders.models import Cart
from .cartitem_serializers import CartItemSerializer


class CartSerializer(serializers.ModelSerializer):
    """ Cart serializer with required fields """
    cart_items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    customer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'restaurant',
                  'cart_items', 'total', 'item_count']
        read_only_fields = ['customer', 'restaurant']

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_total(self, obj):
        """ method to count total amount of cart items. """
        return obj.get_total()

    @extend_schema_field(OpenApiTypes.INT)
    def get_item_count(self, obj):
        """ method to get items count of cart items. """
        return obj.cart_items.count()