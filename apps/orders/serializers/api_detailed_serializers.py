from rest_framework import serializers

from apps.orders.models import Order, OrderItem
from apps.addresses.serializers.api_serializers import AddressSerializer
from apps.products.serializers.api_serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class DetailedOrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    total_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        