from rest_framework import serializers

from apps.addresses.models import Address


class AddressReplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
