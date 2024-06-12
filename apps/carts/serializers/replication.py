from rest_framework import serializers

from apps.carts.models import Cart, CartItem


class CartReplicationSerializer(serializers.ModelSerializer):
    cart_uuid = serializers.UUIDField()
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemReplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
