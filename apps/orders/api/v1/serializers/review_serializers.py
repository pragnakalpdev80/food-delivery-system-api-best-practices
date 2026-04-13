from rest_framework import serializers
from apps.orders.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """ Review serializer with required fields """
    class Meta:
        model = Review
        fields = ['id', 'customer', 'restaurant', 'menu_item', 'order', 'rating', 'comment']  
        read_only_fields = ['id', 'customer']

    def validate_rating(self,value):
        """ rating validation method """
        if value < 1 or value > 5:
            raise serializers.ValidationError("rating should be between 1 and 5")
        return value
    
    def validate(self,data):
        """ 
        This method validates that only order customer can review the delivered order. 
        """
        request = self.context['request']
        order = data.get('order')
        if order.status != 'delivered':
            raise serializers.ValidationError("you can only review delivered orders")
        if order.customer != request.user.customer_profile:
            raise serializers.ValidationError("you can only review your own orders")
        if Review.objects.filter(customer=request.user.customer_profile,order=order).exists():
            raise serializers.ValidationError("you already reviewed this order")
        return data
