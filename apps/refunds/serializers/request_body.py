from rest_framework import serializers

from ..choices import ReturnReason

class CreateRefundSerializer(serializers.Serializer):
    reason_for_return = serializers.ChoiceField(choices=ReturnReason.choices)
    order_id = serializers.UUIDField()
    user_id = serializers.IntegerField()
