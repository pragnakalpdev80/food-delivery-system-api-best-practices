from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from common.utils.validators import validate_quantity
from apps.orders.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """ Cart items serializer with required fields """
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_price = serializers.DecimalField(source='menu_item.price', max_digits=8, decimal_places=2, read_only=True)
    subtotal = serializers.SerializerMethodField()
    quantity = serializers.IntegerField(validators=[validate_quantity])

    class Meta:
        model = CartItem
        fields = ['id', 'menu_item', 'menu_item_name', 'menu_item_price',
                  'quantity', 'special_instructions', 'subtotal']

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_subtotal(self, obj):
        """ method to get subtotal of cart items. """
        return obj.get_subtotal()

    def validate_menu_item(self, value):
        """ 
        Validates the menu items that customer can only add the items from single restaurant only.
        """
        request = self.context.get('request')
        try:
            cart = Cart.objects.get(customer=request.user.customer_profile)
            existing = CartItem.objects.filter(cart=request.user.customer_profile.cart,menu_item=value).first()
            if existing:
                raise serializers.ValidationError(f"Item already exists in your cart.")
        except Cart.DoesNotExist:
            return value
        
        if cart.restaurant and value.restaurant != cart.restaurant:
            raise serializers.ValidationError(f"Clear your cart first to add another restaurant's item.")
        return value
    
    def create(self, validated_data):
        """
        overridden the create method to directly customer can add items without providing his/her own foreign key.
        """
        request = self.context.get('request')
        cart = Cart.objects.get(customer=request.user.customer_profile)
        menu_item = validated_data['menu_item']
        if cart.restaurant is None:
            cart.restaurant = menu_item.restaurant
            cart.save(update_fields=['restaurant', 'updated_at'])

        validated_data['cart'] = cart
        return CartItem.objects.create(**validated_data)
