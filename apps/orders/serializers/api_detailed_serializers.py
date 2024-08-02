from rest_framework import serializers

from apps.orders.models import Order, OrderItem
from apps.addresses.serializers.api_serializers import AddressSerializer
from apps.payments.serializers.api_serializers import PaymentSerializer
from apps.products.serializers.api_serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer for list action, contains list of orders, related address's data and order items' data.
    """
    order_items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    total_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for detail action, contains details of order and related address's data.
    """
    order_items = OrderItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    total_amount_before_tax = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    total_tax = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    total_amount = serializers.SerializerMethodField()

    def get_total_amount(self, obj):
        return round(obj.total_amount_before_tax + obj.total_tax, 2)

    class Meta:
        model = Order
        fields = '__all__'


class OrderSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for detail action, contains details of order without related entities' data, except for order_items.
    """
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_amount_before_tax = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    total_tax = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    total_amount = serializers.SerializerMethodField()

    def get_total_amount(self, obj):
        return round(obj.total_amount_before_tax + obj.total_tax, 2)

    class Meta:
        model = Order
        fields = '__all__'