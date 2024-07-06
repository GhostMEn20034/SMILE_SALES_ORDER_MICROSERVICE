from rest_framework import serializers


class OrderCreationRequestBody(serializers.Serializer):
    cart_owner_id = serializers.IntegerField(min_value=1)
    address_id = serializers.IntegerField(min_value=1)
    product_ids = serializers.ListField(child=serializers.CharField(), required=False)
