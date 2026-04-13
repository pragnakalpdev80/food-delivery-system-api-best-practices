from rest_framework import serializers
from apps.orders.models import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """ order item serializer with required fields """
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menu_item', 'quantity', 'price', 'special_instructions']   

