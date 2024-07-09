from rest_framework import serializers


class CapturePaymentSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
