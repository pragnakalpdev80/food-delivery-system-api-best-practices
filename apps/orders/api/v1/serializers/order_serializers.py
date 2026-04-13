from datetime import datetime, timedelta
from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from apps.orders.models import Cart, Order, OrderItem
from .orderitem_serializers import OrderItemSerializer
from apps.restaurants.api.v1.serializers.restaurant_serializers import RestaurantSerializer


class OrderCreateSerializer(serializers.ModelSerializer):
    """ Order creation serializer with required fields """
    class Meta:
        model = Order
        fields = ['delivery_address', 'special_instructions']

    def validate(self, data):
        """ 
        Order validation method : This method validates customer's address
        """
        request = self.context.get('request')
        address = data.get('delivery_address')
        if address and address.user != request.user:
            raise serializers.ValidationError(
                {'delivery_address': 'This address does not belong to you.'}
            )
        try:
            cart = request.user.customer_profile.cart
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Your cart is empty.")
        
        if not cart.cart_items.exists():
            raise serializers.ValidationError("Your cart is empty.")
        subtotal = cart.get_total()
        if subtotal < cart.restaurant.minimum_order:
            raise serializers.ValidationError(
                f"Minimum order is {cart.restaurant.minimum_order}."
            )        
        data['cart'] = cart
        return data
    
    def create(self, validated_data):
        """ Overrideen create method to add total amount and delivery time of the order with order details. """
        cart = validated_data.pop('cart')
        request = self.context.get('request')
        customer_profile = request.user.customer_profile

        subtotal = cart.get_total()
        delivery_fee = cart.restaurant.delivery_fee
        from decimal import Decimal
        tax = round(subtotal * Decimal(0.18),2)
        total_amount = subtotal + delivery_fee + tax
         # print(cart.restaurant,validated_data)
         # print(datetime.now() + timedelta(seconds=30*60))
        order = Order.objects.create(
            customer=customer_profile,
            restaurant = cart.restaurant,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            tax=tax,
            total_amount=total_amount,
            status='pending',
            estimated_delivery_time= datetime.now() + timedelta(seconds=30*60),
            **validated_data
        )
          # print(order)

        for cart_item in cart.cart_items.select_related('menu_item').all():
            OrderItem.objects.create(
                order=order,
                menu_item=cart_item.menu_item,
                quantity=cart_item.quantity,
                price=cart_item.menu_item.price,
                special_instructions=cart_item.special_instructions
            )

        cart.cart_items.all().delete()
        cart.restaurant = None
        cart.save(update_fields=['restaurant', 'updated_at'])

        return order

class OrderSerializer(serializers.ModelSerializer):
    """ Order serializer with required fields """
    # delivery_address = serializers.CharField(source='delivery_address.address', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'restaurant', 'driver', 'order_number',   
                  'status', 'delivery_address', 'subtotal', 'delivery_fee',
                  'tax', 'total_amount', 'special_instructions',
                  'estimated_delivery_time', 'actual_delivery_time']
        read_only_fields = ['customer', 'order_number', 'subtotal', 'delivery_fee',
                            'tax', 'total_amount', 'estimated_delivery_time', 'actual_delivery_time']


class OrderDetailSerializer(serializers.ModelSerializer):
    """ Order detail serializer with order items and order status. """
    restaurant = RestaurantSerializer(read_only=True)
    menu_item = OrderItemSerializer(read_only=True, many=True)
    customer = serializers.PrimaryKeyRelatedField(read_only=True)
    driver = serializers.PrimaryKeyRelatedField(read_only=True)
    delivery_address = serializers.PrimaryKeyRelatedField(read_only=True)
    can_cancel = serializers.SerializerMethodField()
    is_delivered = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'restaurant', 'driver', 'order_number', 'status',
                  'delivery_address', 'subtotal', 'delivery_fee', 'tax', 'total_amount',
                  'special_instructions', 'estimated_delivery_time', 'actual_delivery_time',
                  'menu_item', 'can_cancel', 'is_delivered']
        read_only_fields = ['customer', 'order_number', 'subtotal', 'delivery_fee',
                            'tax', 'total_amount', 'estimated_delivery_time', 'actual_delivery_time']

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_can_cancel(self, obj):
        """ Method to get order is cancallable or not. """
        return obj.can_cancel()

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_delivered(self, obj):
        """ Method to get the order is delivered or not. """
        return obj.is_delivered() 