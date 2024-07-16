from rest_framework import serializers

from apps.payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
        extra_kwargs = {
            'net_amount': {'write_only': True},
            'provider_fee': {'write_only': True},
            'capture_id': {'write_only': True},
        }
