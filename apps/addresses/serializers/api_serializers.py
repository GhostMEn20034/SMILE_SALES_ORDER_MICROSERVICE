from rest_framework import serializers

from ..models import Address

class AddressSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='original_id')
    oneline_repr = serializers.ReadOnlyField(source='format_address')

    class Meta:
        model = Address
        exclude = ('original_id', )
