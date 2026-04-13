from rest_framework import serializers
from apps.restaurants.models import MenuItem, Restaurant
from common.utils.validators import (
    validate_image_format,
    validate_image_size_5mb,
    validate_amount,
    validate_preparation_time
)

class MenuItemSerializer(serializers.ModelSerializer):
    """ Menu items serializer with required fields """
    image = serializers.ImageField(validators=[validate_image_format, validate_image_size_5mb], required=False) 
    price = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[validate_amount])
    preparation_time = serializers.IntegerField(validators=[validate_preparation_time])

    class Meta:
        model = MenuItem
        fields = ['id', 'restaurant', 'name', 'description', 'price', 'category',
                  'dietary_info', 'image', 'is_available', 'preparation_time']
        read_only_fields = ['restaurant','id']

    def create(self, validated_data):
        """ overridden create method to directly add restaurant owner """
        request = self.context.get('request')
        restaurant = Restaurant.objects.get(owner = request.user)
        validated_data['restaurant'] = restaurant
        return MenuItem.objects.create(**validated_data)
