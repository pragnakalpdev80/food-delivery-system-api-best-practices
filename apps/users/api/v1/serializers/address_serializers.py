from rest_framework import serializers
from apps.users.models import Address

class AddressSerializer(serializers.ModelSerializer):
    """ Customer's address serializer with required fields """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'address_name', 'address', 'is_default', 'user']
        read_only_fields = ['id', 'user']
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return Address.objects.create(**validated_data)
