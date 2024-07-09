from rest_framework import serializers

from apps.payments.models import Payment


class WritePaymentSerializer(serializers.ModelSerializer):
    """
    Payment serializer only for write operations
    """
    class Meta:
        model = Payment
        fields = '__all__'
